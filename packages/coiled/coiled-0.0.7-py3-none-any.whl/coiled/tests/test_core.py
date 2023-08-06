import asyncio
import io
from unittest import mock
from distutils.util import strtobool
from os import environ
import platform
from typing import NamedTuple
import uuid
import yaml

import dask
import pytest
from distributed.utils_test import loop  # noqa: F401
from dask.distributed import Client

from coiled import Cloud, CoiledCluster, Cluster
from users.models import User, Membership, Organization
from backends import in_process
from resources.apps import ResourcesConfig


def skip_in_process_backend_not_on_linux():
    if (
        isinstance(ResourcesConfig.backend, in_process.ClusterManager)
        and platform.system() != "Linux"
    ):
        pytest.skip("TODO: allow for conda solve + build on non-linux platforms")


class UserOrgMembership(NamedTuple):
    user: User
    org: Organization
    membership: Membership


password = "mypassword"
org = "myuser"
configuration = "myclusterconfig"
software_name = "myenv"


@pytest.fixture
async def cleanup(cloud):
    clusters = await cloud.list_clusters()
    await asyncio.gather(*[cloud.delete_cluster(name=name) for name in clusters.keys()])

    yield

    clusters = await cloud.list_clusters()
    await asyncio.gather(*[cloud.delete_cluster(name=name) for name in clusters.keys()])


@pytest.fixture()
def backend():
    """Provide the (in-process) backend as a fixture, and ensure that the rest
    of the application uses it too (we don't need real AWS resources for these
    tests!)"""
    old = ResourcesConfig.backend

    if not strtobool(environ.get("TEST_AGAINST_AWS", "n")):
        new = in_process.ClusterManager()
        ResourcesConfig.backend = new

        yield new

        ResourcesConfig.backend = old
    else:
        yield old


# fixture must be function-scoped because `transactional_db` is
@pytest.fixture(scope="function")
def sample_user(transactional_db, django_user_model, backend, clean_configuration):
    user = django_user_model.objects.create(
        username="myuser", email="myuser@users.com",
    )
    user.set_password(password)
    user.save()
    membership = Membership.objects.filter(user=user).first()
    # Delete default user-level organization. This helps streamline tests.
    # Organization.objects.get(slug="myuser").delete()
    # org = Organization.objects.create(name="Test-MyOrg")
    # membership = Membership.objects.create(
    #     user=user, organization=org, is_admin=True, limit=4
    # )
    return UserOrgMembership(user, membership.organization, membership)


# fixture must be function-scoped because `transactional_db` is
@pytest.fixture(scope="function")
def second_user(transactional_db, django_user_model, backend, clean_configuration):
    user = django_user_model.objects.create(
        username="charlie", email="charlie@users.com",
    )
    user.set_password(password)
    user.save()
    org = Organization.objects.create(name="MyCorp")
    Membership.objects.create(user=user, organization=org, is_admin=True, limit=4)
    return user


@pytest.fixture(scope="function")
def second_org(sample_user):
    org = Organization.objects.create(name="OtherOrg")
    membership = Membership.objects.create(
        user=sample_user.user, organization=org, is_admin=False, limit=2
    )
    sample_user.user.save()
    return UserOrgMembership(sample_user.user, org, membership)


@pytest.fixture(scope="function")
@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
async def cloud(sample_user, clean_configuration):
    async with Cloud(
        sample_user.user.username,
        token=str(sample_user.user.auth_token),
        organization=org,
        asynchronous=True,
    ) as cloud:
        # Remove default software environments and cluster configurations
        default_envs = await cloud.list_software_environments()
        await asyncio.gather(
            *[
                cloud.delete_software_environment(
                    name=name, organization=info["organization"]
                )
                for name, info in default_envs.items()
            ]
        )
        default_configs = await cloud.list_cluster_configurations()
        await asyncio.gather(
            *[
                cloud.delete_cluster_configuration(
                    name=name, organization=info["organization"]
                )
                for name, info in default_configs.items()
            ]
        )

        yield cloud


@pytest.fixture
async def cluster_configuration(cloud, software_env):
    await cloud.create_cluster_configuration(
        name=configuration,
        software=software_env,
        worker_cpu=1,
        worker_memory="2 GiB",
        scheduler_cpu=1,
        scheduler_memory="2 GiB",
    )

    yield configuration

    await cloud.delete_cluster_configuration(name=configuration)

    out = await cloud.list_cluster_configurations(organization=org)
    assert configuration not in out


@pytest.fixture
async def software_env(cloud):
    skip_in_process_backend_not_on_linux()
    if strtobool(environ.get("TEST_AGAINST_AWS", "n")):
        await cloud.create_software_environment(
            name=software_name, container="daskdev/dask:latest"
        )
    else:
        await cloud.create_software_environment(
            name=software_name, conda=["dask", "pandas"]
        )

    yield software_name

    await cloud.delete_software_environment(name=software_name)


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
async def test_basic(sample_user):
    async with Cloud(
        sample_user.user.username,
        token=str(sample_user.user.auth_token),
        asynchronous=True,
    ) as cloud:
        assert cloud.user == sample_user.user.username
        assert org in cloud.organizations
        assert cloud.default_organization == org


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
async def test_default_software_envs_created(sample_user):
    async with Cloud(
        sample_user.user.username,
        token=str(sample_user.user.auth_token),
        asynchronous=True,
    ) as cloud:
        default_envs = await cloud.list_software_environments()
        assert len(default_envs) == 2

        default = default_envs["default"]
        assert default["spec_type"] == "conda"

        assert "conda-forge" in str(default["spec"])
        assert "xarray" in str(default["spec"])

        daskdev = default_envs["daskdev-dask-latest"]
        assert daskdev["spec_type"] == "container"
        assert daskdev["spec"] == "daskdev/dask:latest"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
async def test_default_cluster_configuration_created(sample_user):
    async with Cloud(
        sample_user.user.username,
        token=str(sample_user.user.auth_token),
        asynchronous=True,
    ) as cloud:
        cluster_configs = await cloud.list_cluster_configurations()
        assert len(cluster_configs) == 1
        default = cluster_configs["default"]
        default["organization"] == org
        for process_type in ["scheduler", "worker"]:
            assert default[process_type]["cpu"] == 1
            assert default[process_type]["memory"] == 4
            assert default[process_type]["software"] == "default"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
async def test_trailing_slash(ngrok_url, sample_user):
    async with Cloud(
        sample_user.user.username,
        server=ngrok_url + "/",
        token=str(sample_user.user.auth_token),
        asynchronous=True,
    ):
        pass


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
async def test_server_input(ngrok_url, sample_user):
    async with Cloud(
        sample_user.user.username,
        server=ngrok_url.split("://")[-1],
        token=str(sample_user.user.auth_token),
        asynchronous=True,
    ) as cloud:
        assert cloud.user == sample_user.user.username
        assert org in cloud.organizations
        assert cloud.default_organization == org


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
async def test_informative_error_org(ngrok_url, sample_user):
    with pytest.raises(PermissionError) as info:
        async with Cloud(
            sample_user.user.username,
            server=ngrok_url.split("://")[-1],
            token=str(sample_user.user.auth_token),
            organization="does-not-exist",
            asynchronous=True,
        ):
            pass

    assert sample_user.org.slug in str(info.value)
    assert "does-not-exist" in str(info.value)


@pytest.mark.asyncio
async def test_config(ngrok_url, sample_user):
    with dask.config.set(
        {
            "coiled": {
                "cloud": {
                    "user": sample_user.user.username,
                    "token": str(sample_user.user.auth_token),
                    "server": ngrok_url,
                    "organization": None,
                }
            }
        }
    ):
        async with Cloud(asynchronous=True,) as cloud:
            assert cloud.user == sample_user.user.username
            assert org in cloud.organizations
            assert cloud.default_organization == org


@pytest.mark.asyncio
async def test_repr(cloud, ngrok_url, sample_user):
    for func in [str, repr]:
        assert sample_user.user.username in func(cloud)
        assert ngrok_url in func(cloud)


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
async def test_informative_errors_on_login(sample_user):
    with mock.patch("coiled.core.getpass") as mock_getpass:
        with mock.patch("coiled.core.input") as mock_input:
            mock_input.return_value = "n"
            mock_getpass.return_value = "foo"
            with pytest.raises(Exception) as info:
                await Cloud(
                    sample_user.user.username, asynchronous=True,
                )

            assert "Invalid token" in str(info.value)

    with mock.patch("coiled.core.getpass") as mock_getpass:
        mock_getpass.return_value = "foo"
        with mock.patch("coiled.core.input") as mock_input:
            mock_input.return_value = "n"
            with pytest.raises(Exception) as info:
                await Cloud(
                    "not-a-user", asynchronous=True,
                )
            assert "Invalid token" in str(info.value)

    with pytest.raises(Exception) as info:
        await Cloud(
            sample_user.user.username, token="foo", asynchronous=True,
        )

    assert "Invalid token" in str(info.value)

    with dask.config.set({"coiled.cloud.token": ""}):  # clear any stored token
        with mock.patch("coiled.core.getpass") as mock_getpass:
            mock_getpass.return_value = ""
            with mock.patch("coiled.core.input") as mock_input:
                mock_input.return_value = "n"
                with pytest.raises(Exception) as info:
                    await Cloud(
                        sample_user.user.username, asynchronous=True,
                    )

                assert "Invalid token" in str(info.value)
                assert mock_getpass.called


@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
def test_sync(loop, sample_user, cluster_configuration):
    with Cloud(
        sample_user.user.username, token=str(sample_user.user.auth_token),
    ) as cloud:
        assert cloud.user == sample_user.user.username
        assert org in cloud.organizations

        with CoiledCluster(configuration=cluster_configuration, cloud=cloud) as cluster:
            assert cluster.scale(1) is None


@pytest.mark.asyncio
async def test_cluster_management(cloud, cluster_configuration, cleanup):
    name = f"myname-{uuid.uuid4().hex}"
    result = await cloud.list_clusters()

    try:
        await cloud.create_cluster(
            configuration=configuration, name=name,
        )

        result = await cloud.list_clusters()
        assert name in result

        await cloud.scale(name, n=1)

        async with await cloud.connect(name=name) as client:
            await client.wait_for_workers(1)

            result = await cloud.list_clusters()
            # Check output is formatted properly
            # NOTE that if we're on AWS the scheduler doesn't really knows its
            # own public address, so we get it from the dashboard link
            if strtobool(environ.get("TEST_AGAINST_AWS", "n")):
                address = (
                    client.dashboard_link.replace("/status", "")
                    .replace("8787", "8786")
                    .replace("http", "tls")
                )
            else:
                address = client.scheduler_info()["address"]

            r = result[name]
            assert r["address"] == address
            # TODO this is returning the id of the configuration.
            # We probably don't want that
            assert isinstance(r["configuration"], int)
            assert r["dashboard_address"] == client.dashboard_link.replace(
                "/status", ""
            )
            assert r["organization"] == org
            assert r["status"] == "running"

    finally:
        await cloud.delete_cluster(name=name)

    # wait for the cluster to shut down
    clusters = await cloud.list_clusters()
    for i in range(5):
        if name not in clusters:
            break
        await asyncio.sleep(1)
        clusters = await cloud.list_clusters()

    assert name not in clusters


@pytest.mark.skip(
    reason="Not working right now, and not critical at the moment. Should not block merging PRs."
)
@pytest.mark.asyncio
async def test_no_aws_credentials_warning(cloud, cluster_configuration, cleanup):
    name = "myname"
    environ["AWS_SHARED_CREDENTIALS_FILE"] = "/tmp/nocreds"
    AWS_ACCESS_KEY_ID = environ.pop("AWS_ACCESS_KEY_ID", None)
    AWS_SECRET_ACCESS_KEY = environ.pop("AWS_SECRET_ACCESS_KEY", None)
    await cloud.create_cluster(
        configuration=configuration, name=name,
    )

    with pytest.warns(UserWarning) as records:
        await cloud.connect(name=name)

    assert (
        records[-1].message.args[0]
        == "No AWS credentials found -- none will be sent to the cluster."
    )
    del environ["AWS_SHARED_CREDENTIALS_FILE"]
    if any((AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)):
        environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
        environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
async def test_default_organization(sample_user):
    async with Cloud(
        sample_user.user.username,
        token=str(sample_user.user.auth_token),
        asynchronous=True,
    ) as cloud:
        if len(cloud.organizations) == 1:
            assert cloud.default_organization == org


@pytest.mark.asyncio
async def test_cluster_class(cloud, cluster_configuration, cleanup):
    async with CoiledCluster(
        n_workers=2, asynchronous=True, cloud=cloud, configuration=cluster_configuration
    ) as cluster:
        async with Client(cluster, asynchronous=True, timeout="120 seconds") as client:
            await client.wait_for_workers(2)

            clusters = await cloud.list_clusters()
            assert cluster.name in clusters

    # wait for the cluster to shut down
    clusters = await cloud.list_clusters()
    for i in range(5):
        if cluster.name not in clusters:
            break
        await asyncio.sleep(1)
        clusters = await cloud.list_clusters()

    assert cluster.name not in clusters


@pytest.mark.xfail(reason="We don't support a password keyword currently")
@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
async def test_password_login(sample_user):
    async with Cloud(
        sample_user.user.username, password=password, asynchronous=True,
    ) as cloud:
        assert password not in str(cloud.__dict__)


@pytest.mark.asyncio
async def test_cluster_deprecated(cloud, cluster_configuration, cleanup):
    with pytest.warns(
        DeprecationWarning, match="Cluster has been renamed to CoiledCluster"
    ):
        async with Cluster(
            n_workers=2,
            asynchronous=True,
            cloud=cloud,
            configuration=cluster_configuration,
        ):
            pass


@pytest.mark.asyncio
async def test_scaling_limits(cloud, cleanup, cluster_configuration, sample_user):
    async with CoiledCluster(
        configuration=cluster_configuration, asynchronous=True
    ) as cluster:
        with pytest.raises(Exception) as info:
            await cluster.scale(sample_user.membership.limit * 2)

        assert "limit" in str(info.value)
        assert str(sample_user.membership.limit) in str(info.value)
        assert str(sample_user.membership.limit * 2) in str(info.value)


@pytest.mark.xfail(reason="ValueError not being raised for some reason")
@pytest.mark.asyncio
async def test_default_cloud(sample_user, software_env):
    with pytest.raises(Exception) as info:
        cluster = await CoiledCluster(configuration="foo", asynchronous=True)

    assert "foo" in str(info.value)
    assert "myorg" in str(info.value)

    async with Cloud(
        sample_user.user.username,
        token=str(sample_user.user.auth_token),
        asynchronous=True,
    ):
        async with Cloud(
            sample_user.user.username,
            token=str(sample_user.user.auth_token),
            asynchronous=True,
        ) as cloud_2:
            await cloud_2.create_cluster_configuration(
                name=configuration, worker_cpu=1, software=software_env,
            )
            try:
                cluster = CoiledCluster(configuration=configuration, asynchronous=True)
                assert cluster.cloud is cloud_2
            finally:
                await cloud_2.delete_cluster_configuration(name=configuration)


@pytest.mark.asyncio
async def test_cloud_repr_html(cloud):
    text = cloud._repr_html_()
    assert cloud.user in text
    assert cloud.server in text
    assert cloud.default_organization in text


@pytest.mark.xfail(reason="TODO: support pip software environments", strict=True)
@pytest.mark.asyncio
async def test_software_environment_pip(cloud, cleanup, sample_user, tmp_path):

    packages = ["dask==2.15", "xarray", "pandas"]
    # Provide a list of packages
    await cloud.create_software_environment(name="env-1", pip=packages)

    result = await cloud.list_software_environments()
    # Check output is formatted properly
    expected = {
        "env-1": {"organization": org, "spec": "\n".join(packages), "spec_type": "pip"}
    }
    assert result == expected


@pytest.mark.asyncio
async def test_software_environment_conda(cloud, cleanup, sample_user, tmp_path):
    skip_in_process_backend_not_on_linux()
    # below is what yaml.load(<env-file>) gives
    conda_env = {
        "channels": ["conda-forge"],
        "dependencies": [
            "dask=2.15",
            "xarray",
            "pandas",
            # TODO: support pip packages within a conda environment file
            # conda supports this via their CLI, but not when using conda.api.Solver
            # {"pip": ["numpy", "matplotlib"]},
        ],
    }

    # Provide a data structure
    await cloud.create_software_environment(name="env-1", conda=conda_env)

    result = await cloud.list_software_environments()

    # Check output is formatted properly
    assert len(result) == 1
    assert result["env-1"]["organization"] == org
    assert result["env-1"]["spec"] == str(conda_env)
    assert result["env-1"]["spec_type"] == "conda"

    # Provide a local environment file
    environment_file = tmp_path / "environment.yml"
    with environment_file.open(mode="w") as f:
        f.writelines(yaml.dump(conda_env))

    await cloud.create_software_environment(name="env-2", conda=environment_file)

    result = await cloud.list_software_environments()

    # Check output is formatted properly
    assert len(result) == 2
    assert result["env-2"]["organization"] == org
    assert result["env-2"]["spec"] == str(conda_env)
    assert result["env-2"]["spec_type"] == "conda"


@pytest.mark.asyncio
async def test_software_environment_container(cloud, cleanup, sample_user, tmp_path):

    # Provide docker image URI
    await cloud.create_software_environment(
        name="env-1", container="daskdev/dask:latest"
    )

    result = await cloud.list_software_environments()
    # Check output is formatted properly
    expected = {
        "env-1": {
            "organization": org,
            "spec": "daskdev/dask:latest",
            "spec_type": "container",
        }
    }
    assert result == expected


@pytest.mark.asyncio
async def test_delete_software_environment(cloud, cleanup, sample_user):
    skip_in_process_backend_not_on_linux()
    # Initially no software environments
    result = await cloud.list_software_environments()
    assert not result

    packages = ["dask==2.15", "xarray", "pandas"]

    # Create two configurations
    await cloud.create_software_environment(name="env-1", conda=packages)
    await cloud.create_software_environment(name="env-2", conda=packages)

    result = await cloud.list_software_environments()
    assert len(result) == 2

    # Delete one of the configurations
    await cloud.delete_software_environment(name="env-1")
    result = await cloud.list_software_environments()
    assert len(result) == 1
    assert "env-2" in result


@pytest.mark.asyncio
async def test_create_and_list_cluster_configuration(
    cloud, cleanup, sample_user, software_env
):
    # TODO decide on defaults and who should own them (defaults in the REST API
    # or maybe just the sdk client)

    # Create basic cluster configuration
    # await cloud.create_cluster_configuration(name="config-1")

    # Create a more customized cluster configuration
    await cloud.create_cluster_configuration(
        name="config-2",
        software=software_env,
        worker_cpu=3,
        worker_memory="3 GiB",
        scheduler_cpu=2,
        scheduler_memory="2 GiB",
        environment={"foo": "bar"},
    )

    result = await cloud.list_cluster_configurations()

    # Check output is formatted properly
    expected = {
        "config-2": {
            "organization": org,
            "scheduler": {"cpu": 2, "memory": 2, "software": software_name},
            "worker": {"cpu": 3, "memory": 3, "software": software_name},
        }
    }
    assert result == expected


@pytest.mark.asyncio
async def test_delete_cluster_configuration(cloud, cleanup, sample_user, software_env):
    # Initially no configurations
    result = await cloud.list_cluster_configurations()
    assert not result

    # Create two configurations
    await cloud.create_cluster_configuration(
        name="config-1",
        software=software_env,
        worker_cpu=1,
        worker_memory="1 GiB",
        environment={"foo": "bar"},
    )
    await cloud.create_cluster_configuration(
        name="config-2",
        software=software_env,
        worker_cpu=2,
        worker_memory="2 GiB",
        environment={"foo": "bar"},
    )

    result = await cloud.list_cluster_configurations()
    assert len(result) == 2

    # Delete one of the configurations
    await cloud.delete_cluster_configuration(name="config-1")
    result = await cloud.list_cluster_configurations()
    assert len(result) == 1
    assert "config-2" in result


@pytest.mark.asyncio
async def test_docker_images(cloud, cleanup, sample_user, tmp_path, backend):
    if isinstance(backend, in_process.ClusterManager):
        raise pytest.skip()

    await cloud.create_software_environment(
        name="env-1",
        conda={
            "channels": ["conda-forge", "defaults"],
            "dependencies": ["python=3.8", "dask=2.19.0", "sparse"],
        },
    )
    await cloud.create_cluster_configuration(
        name=configuration, software="env-1", worker_cpu=1, worker_memory="2 GiB",
    )

    async with CoiledCluster(asynchronous=True, configuration=configuration) as cluster:
        async with Client(cluster, asynchronous=True) as client:

            def test_import():
                try:
                    import sparse  # noqa: F401

                    return True
                except ImportError:
                    return False

            result = await client.run_on_scheduler(test_import)
            assert result


@pytest.mark.asyncio
async def test_current(sample_user):
    with pytest.raises(Exception):
        await Cloud.current()

    with pytest.raises(Exception):
        await CoiledCluster(configuration="default", asynchronous=True)

    with dask.config.set(
        {
            "coiled.cloud.user": sample_user.user.username,
            "coiled.cloud.token": str(sample_user.user.auth_token),
        }
    ):
        await Cloud.current()
        # await CoiledCluster(configuration="default", asynchronous=True)  # no cluster config


@pytest.mark.asyncio
async def test_update_software_environment_conda(cloud, cleanup, sample_user, tmp_path):
    skip_in_process_backend_not_on_linux()
    # below is what yaml.load(<env-file>) gives
    out = io.StringIO()
    conda_env = {
        "channels": ["defaults"],
        "dependencies": [
            "dask==2.15",
            "xarray",
            "pandas",
            # TODO is this how we want to handle pip installs within conda?
            # {"pip": ["numpy", "matplotlib"]},
        ],
    }

    await cloud.create_software_environment(name="env-1", conda=conda_env)

    await cloud.create_software_environment(
        name="env-1", conda=conda_env, log_output=out
    )

    assert not out.tell()

    conda_env = {
        "channels": ["defaults"],
        "dependencies": ["dask", "xarray", "pandas",],
    }

    await cloud.create_software_environment(
        name="env-1", conda=conda_env, log_output=out
    )

    out.seek(0)
    text = out.read()
    assert "conda" in text.lower()
    assert "success" in text.lower()

    conda_env = {
        "channels": ["defaults"],
        "dependencies": ["dask", "not-a-package", "pandas",],
    }

    out = io.StringIO()
    with pytest.raises(Exception):
        await cloud.create_software_environment(
            name="env-1", conda=conda_env, log_output=out
        )
    out.seek(0)
    text = out.read()
    assert "failed" in text.lower()


@pytest.mark.asyncio
async def test_default_org_username(second_user, clean_configuration):
    async with Cloud(
        second_user.username, token=str(second_user.auth_token), asynchronous=True,
    ) as cloud:
        assert cloud.default_organization == second_user.username


@pytest.mark.asyncio
async def test_organization_config(sample_user, second_org):
    with dask.config.set({"coiled.cloud.organization": second_org.org.slug}):
        async with Cloud(
            sample_user.user.username,
            token=str(sample_user.user.auth_token),
            asynchronous=True,
        ) as cloud:
            assert cloud.default_organization == second_org.org.slug


@pytest.mark.asyncio
async def tests_list_clusters_organization(
    sample_user, second_org, cloud, cluster_configuration
):
    # Create cluster in first organization
    await cloud.create_cluster(
        name="cluster-1",
        configuration=cluster_configuration,
        organization=sample_user.org.slug,
    )

    # Creat cluster in second organization
    await cloud.create_software_environment(
        name="env-2", conda=["toolz"], organization=second_org.org.slug
    )
    await cloud.create_cluster_configuration(
        name="config-2", software="env-2", organization=second_org.org.slug
    )
    await cloud.create_cluster(
        name="cluster-2", configuration="config-2", organization=second_org.org.slug
    )

    # Ensure organization= in list_clusters filters by the specified organization
    result = await cloud.list_clusters(organization=second_org.org.slug)
    assert len(result) == 1
    assert "cluster-2" in result

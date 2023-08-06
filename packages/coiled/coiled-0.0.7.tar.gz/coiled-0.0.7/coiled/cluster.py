import asyncio
import uuid
import warnings

import dask.distributed
import distributed.deploy

from .core import Cloud


class CoiledCluster(distributed.deploy.Cluster):
    """ Create a Dask cluster with Coiled Cloud

    Parameters
    ----------
    n_workers
        Number of workers in this cluster. Defaults to 4.
    configuration
        Name of cluster configuration to create cluster from.
        Defaults to ``"default"``.
    name
        Name to use for identifying this cluster. Defaults to ``None``.
    asynchronous
        Set to True if using this Cloud within ``async``/``await`` functions or
        within Tornado ``gen.coroutines``. Otherwise this should remain
        ``False`` for normal use. Default is ``False``.
    cloud
        Cloud object to use for interacting with Coiled Cloud.
    organization
        Name of Coiled Cloud orgnaization to use. If not provided, will
        default to the user organization for the ``cloud`` object being used.
    """

    def __init__(
        self,
        n_workers: int = 4,
        configuration: str = "default",
        name: str = None,
        asynchronous: bool = False,
        cloud: Cloud = None,
        organization: str = None,
    ):
        # we really need to call this first before any of the below code errors
        # out; otherwise because of the fact that this object inherits from
        # deploy.Cloud __del__ (and perhaps __repr__) will have AttributeErrors
        # because the gc will run and attributes like `.status` and
        # `.scheduler_comm` will not have been assigned to the object's instance
        # yet
        super().__init__(asynchronous=asynchronous)

        self.cloud = cloud or Cloud.current(asynchronous=asynchronous)
        self.configuration = configuration
        self.name = name
        self.organization = organization
        self._start_n_workers = n_workers
        self._lock = asyncio.Lock(loop=self.loop)
        self._asynchronous = asynchronous

        if not self.asynchronous:
            self.sync(self._start)

    @property
    def loop(self):
        return self.cloud.loop

    async def _start(self):
        self.cloud = await self.cloud
        self.name = self.name or self.cloud.user + "-" + str(uuid.uuid4())[:10]
        print("Creating cluster. This takes about a minute")  # TODO: add timer
        await self.cloud.create_cluster(
            organization=self.organization,
            configuration=self.configuration,
            name=self.name,
        )
        if self._start_n_workers:
            await self._scale(self._start_n_workers)

        self.security, info = await self.cloud.security(name=self.name, organization=self.organization)  # type: ignore

        self.scheduler_comm = dask.distributed.rpc(
            info["public_address"],
            connection_args=self.security.get_connection_args("client"),
        )

        await super()._start()

    def __await__(self):
        async def _():
            async with self._lock:
                if self.status == "created":
                    await self._start()
                assert self.status == "running"
            return self

        return _().__await__()

    async def _close(self):
        await self.cloud.delete_cluster(
            organization=self.organization, name=self.name,
        )
        await super()._close()

    async def _scale(self, n: int) -> None:
        await self.cloud.scale(organization=self.organization, name=self.name, n=n)  # type: ignore

    def scale(self, n: int) -> None:
        """ Scale cluster to ``n`` workers

        Parameters
        ----------
        n
            Number of workers to scale cluster size to.
        """
        return self.sync(self._scale, n=n)

    def __enter__(self):
        return self.sync(self.__aenter__)

    def __exit__(self, *args, **kwargs):
        return self.sync(self.__aexit__, *args, **kwargs)


class Cluster(CoiledCluster):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "Cluster has been renamed to CoiledCluster. Please "
            "switch to using CoiledCluster as Cluster will be "
            "removed in a future release.",
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)

=============
Core Concepts
=============

.. currentmodule:: coiled

This page covers the core concepts and functionality of Coiled Cloud.
To demonstrate these features, we'll walk through the example worflow below
which uses the ``coiled`` Python package to manage custom software environments,
manage cluster configurations, and spin up a remote Dask cluster.

.. _example-workflow:

Example workflow
----------------

Below is an example workflow using the ``coiled`` Python package.
The following sections will discuss each portion of this example step-by-step.

.. code-block:: python

    from coiled import Cloud, CoiledCluster

    # Connect to Coiled Cloud by creaeting a Cloud instance
    cloud = Cloud()

    # Create a new software environment with the libraries you want
    cloud.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray==0.15.1", "numba"]
    )

    # Control the resources of your cluster by creating a new cluster configuration
    cloud.create_cluster_configuration(
        name="my-cluster-config",
        worker_memory="16 GiB",
        worker_cpu=4,
        scheduler_memory="4 GiB",
        scheduler_cpu=1,
        software="my-conda-env",
    )

    # Spin up a Dask cluster using
    cluster = CoiledCluster(n_workers=5, configuration="my-cluster-config")

    # Connect a Dask Client to your cluster to perform computations on the cluster
    from dask.distributed import Client

    client = Client(cluster)

.. _cloud:

Connecting to Coiled Cloud
--------------------------

The :class:`Cloud` object is how you connect to and interact with Coiled Cloud.
To create a ``Cloud`` object, provide your Coiled Cloud account username:

.. code-block:: python

    from coiled import Cloud

    cloud = Cloud()

You'll then be prompted to enter your account credentials and, optionally, save your
credentials to a :doc:`configuration file <configuration>` to avoid
the need to enter them each time you create a ``Cloud`` object.


.. _software-envs:

Software environments
---------------------

A crucial part of doing your work is making sure you have the software packages
you need. You can manage software environments with Coiled Cloud by providing a
name for a given software environment as well as a specification for what
packages should be installed in the environment. Specifically, Coiled Cloud
supports building software environments with
`conda <https://docs.conda.io/en/latest/>`_,
`pip <https://pip.pypa.io/en/stable/>`_, or Docker. Any software environment
can then be easily deployed for use in a Dask cluster.

.. note::

    When you create your Coiled Cloud account you'll have two software
    environments available: a "default" environment and a
    "daskdev-dask-latest" environment. The "default" software environment
    has Dask and a few other packages installed (e.g. NumPy, Pandas, Bokeh).
    The "daskdev-dask-latest" software environment is built from the
    ``daskdev/dask:latest`` `Docker image <https://hub.docker.com/r/daskdev/dask>`_.


Conda
^^^^^

To create a software environment using conda, use the ``conda=`` keyword
argument of :meth:`Cloud.create_software_environment` to specify a list of
packages to install into the environment. From our
:ref:`example workflow <example-workflow>`:

.. code-block:: python

    cloud.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray==0.15.1", "numba"]
    )

will build a software environment named "my-conda-env" and use conda to
install dask, version 0.15.1 of xarray, and numba from the ``defaults`` conda
channel. More complex package specifications, like installing packages from
additional conda channels, are supported by passing a dictionary to ``conda=``.
For example, to search for packages in both the ``conda-forge`` and
``defaults`` channels:

.. code-block::

    cloud.create_software_environment(name="my-conda-env",
                                      conda={"channels": ["conda-forge", "defaults"],
                                             "dependencies": ["dask", "xarray=0.15.1", "numba"]})

Equivalently, you can also provide an input conda environment YAML file:

.. code-block:: python

    cloud.create_software_environment(name="my-conda-env", conda="environment.yml")

where ``environment.yml`` is a local file with the following content:

.. code-block:: yaml

    # environment.yml
    channels:
      - conda-forge
      - defaults
    dependencies:
      - dask
      - xarray=0.15.1
      - numba


Pip
^^^

To create a software environment using pip, use the ``pip=`` keyword argument of
:meth:`Cloud.create_software_environment` to specify a list of packages
(on `PyPI <https://pypi.org/>`_) to install into the environment. For example:

.. code-block:: python

    cloud.create_software_environment(
        name="my-pip-env", pip=["dask", "xarray==0.15.1", "numba"]
    )

will build a software environment named "my-pip-env" and use pip to
install dask, version 0.15.1 of xarray, and numba. Equivalently, you can also
provide an input pip requirements file if you prefer:

.. code-block:: python

    cloud.create_software_environment(name="my-pip-env", pip="requirements.txt")

where ``requirements.txt`` is a local file with the following content:

.. code-block::

    # requirements.txt
    dask
    xarray==0.15.1
    numba


Docker
^^^^^^

Any Docker image on `Docker Hub <https://hub.docker.com/>`_ can be used to
build a custom software environment for your cluster by using the ``container=``
keyword argument of of :meth:`Cloud.create_software_environment`.
For example:

.. code-block::

    cloud.create_software_environment(name="my-docker-env",
                                      container="rapidsai/rapidsai:latest")

will build a software environment named "my-docker-env" using latest
RAPIDS Docker image.


Listing and deleting software environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :meth:`Cloud.list_software_environments` method will list all available
software environments:

.. code-block:: python

    cloud.list_software_environments()

While :meth:`Cloud.delete_software_environment` can be used to delete
individual software environments. For example:

.. code-block:: python

    cloud.delete_software_environments(name="my-pip-env")

will delete the software environment named "my-pip-env".


Creating Coiled conda software environments locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``coiled`` comes with a command line interface, ``coiled env create``, for creating
a Coiled Cloud conda software environment locally on your machine. This is useful
for matching the software environment used locally (e.g. on your laptop) with the
software environment being used on your remote Dask cluster.

For example:

.. code-block:: bash

    # Create local version of the coiled/default software environment
    coiled env create coiled/default

    # Activate the conda environment
    conda activate coiled-default

The ``coiled/default`` name after ``coiled env create`` specifies which Coiled Cloud
software environment should be created locally. Generally Coiled Cloud software environments
are specified in the form of "<coiled-account-name>/<software-environment-name>".
So in the above example we're telling ``coiled env create`` to create the Coiled
software environment named "default" in the "coiled" account locally.

Additionally, there is a ``--name`` option to specify the name of the locally created conda environment.
By default, if not specified, "<coiled-account-name>-<software-environment-name>" will be used.
So ``coiled env create coiled/default`` will create a local conda environment named "coiled-default",
while ``coiled env create --name "myenv" coiled/default`` creates a local conda environment
named "myenv".


.. _cluster-config:

Cluster configurations
----------------------

Cluster configurations let you specify the resources a cluster will be launched
on. Specifically, you can configure the number of CPUs, memory, and software
environment for the scheduler and workers in a cluster.

It's important to note that creating a cluster configuration doesn't create a
cluster or provision any resources. You can think of a cluster configuration as
a template, or recipe, for a cluster that you can create later
(see the :ref:`cluster-creation` section for how to create a cluster from a
cluster configuration).

Creating cluster configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cluster configurations are created using the
:meth:`Cloud.create_cluster_configuration` method. From our
:ref:`example workflow <example-workflow>`:

.. code-block:: python

    # Create "my-conda-env" software environment
    cloud.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray==0.15.1", "numba"]
    )

    # Create "my-cluster-config" cluster configuration
    cloud.create_cluster_configuration(
        name="my-cluster-config",
        worker_memory="16 GiB",
        worker_cpu=4,
        scheduler_memory="4 GiB",
        scheduler_cpu=1,
        software="daskdev-dask-latest",
    )

creates a cluster configuration named "my-cluster-config" where the scheduler
has 1 CPU / 4 GiB of memory, workers each have 4 CPUs / 16 GiB of memory, and
the "daskdev-dask-latest" software environment is used for the scheduler
and all workers.

.. note::

    When you create your Coiled Cloud account you'll have a "default"
    cluster configuration available which uses 1 CPU and 4 GiB of memory for
    the scheduler and all workers as well as the "default" software
    environment.


Listing and deleting cluster configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :meth:`Cloud.list_cluster_configurations` method will list all available
cluster configurations:

.. code-block:: python

    cloud.list_cluster_configurations()

While :meth:`Cloud.delete_cluster_configuration` can be used to delete
individual configurations. For example:

.. code-block:: python

    cloud.delete_cluster_configuration(name="my-cluster-config")

deletes the cluster configuration named "my-cluster-config".


.. _cluster-creation:

Creating a cluster
------------------

Creating a Dask cluster on cloud resources is done with the
:class:`CoiledCluster` object. ``CoiledCluster`` manages your Dask cluster
much like other cluster object you may have seen before like
:class:`distributed.LocalCluster` or :class:`dask_kubernetes.KubeCluster`.
From our :ref:`example workflow <example-workflow>`:

.. code-block:: python

    from coiled import CoiledCluster

    cluster = CoiledCluster(n_workers=5, configuration="my-cluster-config")

will create a cluster with 5 workers, each with resources based on the cluster
configuration named "my-cluster-config". If no ``configuration=`` is specified,
then the "default" cluster configuration will be used.

.. note::

    Creating a cluster involves provisioning various resources on cloud-based
    infrastructure. This process takes about a minute in most cases.

Once a cluster has been created, you can attach a :class:`distributed.Client`
to the cluster and start submitting tasks:

.. code-block:: python

    from dask.distributed import Client

    client = Client(cluster)

To view the
`Dask diagnostic dashboard <https://docs.dask.org/en/latest/diagnostics-distributed.html>`_
for your cluster, navigate to the cluster's ``dashboard_link``:

.. code-block:: python

    cluster.dashboard_link

which should output an address along the lines of
``"https://ec2-...compute.amazonaws.com:8787/status"``.


Listing and deleting clusters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :meth:`Cloud.list_clusters` method will list all active clusters:

.. code-block:: python

    cloud.list_clusters()

Note that when a cluster is created, by default, a unique name for the cluster
is automatically generated. You can provide your own cluster name using the
``name=`` keyword argument for ``CoiledCluster``.

:meth:`Cloud.delete_cluster` can be used to delete individual clusters.
For example:

.. code-block:: python

    cloud.delete_cluster(name="my-cluster")

deletes the cluster named "my-cluster".

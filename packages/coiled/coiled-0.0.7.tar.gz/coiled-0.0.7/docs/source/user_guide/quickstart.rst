==========
Quickstart
==========

.. currentmodule:: coiled

After :ref:`installing <install>` the ``coiled`` Python package, you can
connect to Coiled Cloud by creating a :class:`Cloud` object with your account
username and token:

.. code-block:: python

   from coiled import Cloud

   cloud = Cloud(user="alice", token="my-secret-token")

Next spin up a Dask cluster by creating a :class:`CoiledCluster`:

.. code-block:: python

   from coiled import CoiledCluster

   cluster = CoiledCluster(cloud=cloud)

Note that when creating a ``CoiledCluster``, resources for our Dask cluster are
provisioned on AWS. This provisioning process takes about a minute to complete.
Once our cluster is created, we can then connect to it with a Dask distributed
``Client``:

.. code-block:: python

   from dask.distributed import Client

   client = Client(cluster)

and submit tasks to our remote cluster.

**Next steps**

This page shows how to get a simple Dask cluster up and running with Coiled
Cloud. In everyday use, there are lots of other things you'll also want
to do. Like creating custom software environments with the packages you need
and configuring the specifics of your cluster (e.g. the amount of memory each
worker has). Information on these features, and more, is found over on the
:doc:`concepts` page.

Happy computing!

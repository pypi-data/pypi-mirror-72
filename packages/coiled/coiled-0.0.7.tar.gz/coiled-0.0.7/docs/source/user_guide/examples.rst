========
Examples
========

.. _jupyterlab-extension:

Using the Dask JupyterLab extension
-----------------------------------

Dask maintains a `JupyterLab extension <https://github.com/dask/dask-labextension>`_ which allows
`Dask dashboard plots <https://docs.dask.org/en/latest/diagnostics-distributed.html>`_ to be
embedded directly into JupyterLab. Using the extension involves two steps: installing the
JupyterLab extension and connecting to your Coiled Cloud cluster.

**Installation**

To install the Dask JupyterLab extension first install the ``dask-labextension`` package, for
example, with the ``conda`` package manager:

.. code-block::

    conda install -c conda-forge dask-labextension

Next register the JupyterLab extension with your JupyterLab installation:

.. code-block::

    jupyter labextension install dask-labextension

**Connecting to your cluster**

Now you can connect the extension to your Coiled Cloud cluster by copying the Dask dashboard URL
for your ``CoiledCluster`` (which is available via the ``.dashboard_link`` attribute) into the
Dask tab in the JupyterLab left sidebar.

.. figure:: images/labextension.png

Dashboard plots are now available for you to embed directly into your JupyterLab session!
Interactive plots are accessible by clicking the orange button with each plot's name like "progress"
or "task stream".

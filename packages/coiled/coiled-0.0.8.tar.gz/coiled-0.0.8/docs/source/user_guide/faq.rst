===
FAQ
===


- :ref:`version-mismatch-warning`


.. _version-mismatch-warning:

Why do I see a version mismatch warning?
----------------------------------------

Dask will emit a warning when it finds multiple versions of the same package on a cluster.
When using Coiled Cloud this most often means there's a version mismatch between a package in
your local environment and the remote cluster environment. For example, you might have NumPy 1.18.2
installed in your local Python environment on your laptop, while the remote Dask cluster on AWS
has NumPy 1.18.4 installed.

Ensuring package versions match is something that we're working on. In the meantime you might
want to install the following packages locally:

.. code-block::

    conda install --yes \
        -c conda-forge \
        python==3.8 \
        python-blosc \
        cytoolz \
        dask==2.16.0 \
        lz4 \
        nomkl \
        numpy==1.18.1 \
        pandas==1.0.1

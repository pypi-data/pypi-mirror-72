=============
Configuration
=============

``coiled`` uses Dask's built in
`configuration system <https://docs.dask.org/en/latest/configuration.html>`_
to manage configuration options. Namely, configuration settings can be set:

- In the configuration file ``~/.config/dask/coiled.yaml``
- Using environment variables like ``DASK_COILED__CLOUD__USER="alice"``
- Configured directly in Python code using ``dask.config.set``


Configuration reference
-----------------------

The YAML snippet below shows the possible configuration options, along with
their default values:

.. code-block:: yaml

    coiled:
      cloud:
        user: ""                           # Default username
        token: ""                          # Default token
        server: https://dev.coiledhq.com   # Default server

    distributed:
      scheduler:
        preload: https://dev.coiledhq.com/preloads/insights.py

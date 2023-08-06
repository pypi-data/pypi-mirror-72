Coiled Cloud Python API
=======================

See [coiled.io](https://coiled.io)

Example
-------

```python
from coiled import Cloud, CoiledCluster

cloud = Cloud(user="alice", token="my-secret-token",)

cluster = CoiledCluster(
    organization="my-corp", configuration="production", name="experiment-1",
)

from dask.distributed import Client

client = Client(cluster)
```

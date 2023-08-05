# pullframe
[![pypi](https://img.shields.io/pypi/v/pullframe.svg)](https://pypi.python.org/pypi/pullframe)
[![Build Status](https://travis-ci.com/ghsang/pullframe.svg?branch=master)](https://travis-ci.com/ghsang/pullframe)
[![codecov](https://codecov.io/gh/ghsang/pullframe/branch/master/graph/badge.svg)](https://codecov.io/gh/ghsang/pullframe)

## pull based pandas dataframe syncing
-----
To reduce network consumption, it syncs dataframe from the other nodes only on demand.
When your task is divide and conquer style, you should consider [dask][1] instead.

### Features
* Once the cache has been synced, it will not call remotes. So cache's locality is 1.
* Ideal situations is that you need to read some dataframe multiple times on serveral nodes and the data frame should be updated frequently.
* Only unique str name is required configuration when you add a new dataframe on the system.
* No configuration, no operation is needed when a new node is added and a node is crashed and restored.
* No configuration, no operation makes it be easy to scale up in the cloud.


### Communications
* Coordination via zookeeper
* Synchronize files via http POST


#### Start Service
```
$ uvicorn pullframe.sender:app
```

### Example

#### Load / Save
```
from pullframe import pullframe

with pullframe(hosts, directory, sync_timeo 60.0) as pf:
    # set start as None if you want to load from the very beginning
    # set end as None if you want to load from the very ending
    df = pf.load(name, start: Optional[datetime], end: Optional[datetime])

    pf.save(name, df)

```

### TODO
* Check cache discrepency/corruption between nodes.
* Stable backup using Amazon S3 / Google cloud storage.
* Replace zookeeper client to zake (fake kazoo client) during tests.

### Requirements
* zookeeper
* the dataframe's index should be datetime
* linux
* python>=3.7
* python = "^3.7"
* pandas = "^1.0.0"
* tables = "^3.6.1"
* fastapi = "^0.58.0"
* aiofiles = "^0.5.0"
* kazoo = "^2.7.0"

### Free software: MIT License

### Credits

* This package was created with [Cookiecutter][2]
* Also was copied and modified from the [audreyr/cookiecutter-pypackage][3] project template.

[1]: https://dask.org
[2]: https://github.com/cookiecutter/cookiecutter
[3]: https://github.com/audreyr/cookiecutter-pypackage

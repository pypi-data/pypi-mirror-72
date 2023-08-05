# ClickHouse Pool for Python

A thread-safe connection pool for ClickHouse. Inspired by `psycopg2` and using
[`clickhouse-driver`](https://github.com/mymarilyn/clickhouse-driver) for
connections.

## Installation

`pip install clickhouse-pool`

## Quick Start

```python
from clickhouse_pool.pool import ChPool

# create a pool
pool = ChPool()

# get a clickhouse-driver client
with pool.get_client() as client:
    # execute sql and print the result
    result = client.execute("SELECT * FROM system.numbers LIMIT 5")
    print(result)

# always close all connections in the pool once you're done with it
pool.close_all_connections()
```

## Connection Pool Size

To change the connection pool size,

```python
# create a pool with minimum 20 connections and a max of 40
pool = ChPool(connections_min=20, connections_max=40)

# get a clickhouse-driver client
with pool.get_client() as client:
    # execute sql and print the result
    result = client.execute("SELECT * FROM system.numbers LIMIT 5")
    print(result)

# always close all connections in the pool once you're done with it
pool.close_all_connections()
```

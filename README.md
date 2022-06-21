# Load balancing experiments

Some tests as to what a load balancing strategy that optimizes for both
cache-locality and even load could look like.

A few rather naive approaches are implemented in `algorithms.py`. Some of them
hold state that is assumed to be reset every `n` seconds, and is local to e.g.
a Kafka producer/HTTP client.

## Running tests

Just run `make`. It will create a virtualenv, add dependencies, execute the tests and show some graphs.

## Reading the graphs

Each column is a separate load balancing strategy. The rows have the following meaning:

* `total ids`: "IDs" are representing the resource one would want to
  load-balance by, for example in Sentry's Relay there are per-DSN caches, so
  this would be a stand-in for the DSN. The histogram shows how IDs are
  distributed across traffic: It's assumed that a few IDs are responsible for a
  large amount of traffic, and that there is a long tail.

  The same input data is used for all tests, so as a byproduct of that this
  graph is repeated `n` times in that row.

* `requests per slot, <classname>`: Histogram of how traffic ends up being
  distributed under this strategy. A flat-top, rectangle-like graph means
  evenly distributed traffic (in terms of number of messages). "Slots" are
  partitions/shards/nodes that traffic is "sorted" into.

  Examples:

  * `Hashed` pretty much mirrors the distribution of IDs, and as such traffic
    is not evenly distributed

  * `Randomized` is doing okay with distributing load evenly.

* `ids per slot`: How many distinct IDs are observed in each slot. A lower
  number for each bar means better cache locality. Uneven distribution of
  number of IDs is also probably bad for evenly distributing load across nodes.

  Examples:

  * `Randomized` also distributes IDs evenly across nodes, however each node
    has to deal with a large amount of unique IDs.

  * `Hashed` ensures that one node does not need to deal with many unique IDs,
    and that's great for cache locality.

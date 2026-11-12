# Why we removed our cache

In June we put a Redis read-through cache in front of Postgres for our busiest read endpoint, and in October we took it out. While the cache was in place, median latency improved, but p99 rose from 41 ms to 67 ms. After removing it and fixing the underlying query, p99 is 19 ms.

## The setup

The endpoint is `GET /v1/accounts/:id/summary`. It peaks around 2,400 requests per second and runs a four-table join on Postgres 16, served by a primary and two replicas. Before the cache, p50 was 6 ms and p99 was 41 ms.

The cache was textbook. A request looked up the key in Redis. On a miss, it ran the query, serialized the result as JSON, and wrote it back with a five-minute TTL. A write to an account deleted its key.

Within a week the hit rate settled at 83% and p50 dropped to 1.8 ms. We announced the win and moved on.

## What the dashboard hid

We tracked two numbers: hit rate and blended p50. Both looked good. p99 crept upward over the following months, and we blamed traffic growth, which was real (about 30% over the period).

We only split latency by hit and miss after a customer reported timeouts on their largest account. Hits had a p99 of 4 ms. Misses had a p99 of 140 ms.

With a 17% miss rate, the overall p99 sits at roughly the 94th percentile of the miss path. Hits have no influence on it. We had made the fast 83% of requests faster and the slow 17% slower.

## Why a miss was slower than no cache

**The miss path does more work.** A miss costs a Redis GET, the same Postgres query as before, JSON serialization, and a Redis SET. The keys that miss are the rarely read accounts, whose rows are least likely to be in Postgres's buffer cache. Those were already our slowest requests. The cache couldn't help them, because a rarely read key has usually expired before anyone reads it again.

**Large values stalled Redis.** The median summary is 3 KB, but our biggest accounts produce 4 to 6 MB of JSON. Redis executes commands on a single thread, so while it moves a 6 MB value, every other client waits. During bursts of large-account traffic, client-observed Redis p99 went from 0.4 ms to 11 ms, and a miss paid that twice.

**Expiry caused stampedes.** When a hot key's TTL ran out, 30 or 40 concurrent requests missed together and each ran the join. A nightly billing job also touched about 300,000 accounts and deleted their keys, so every morning's traffic ramp met a mostly cold cache. We added a per-key lock so that only one request rebuilt the value. That cut Postgres load, but when the rebuilding request was slow, every request waiting on it was slow too.

## What we did instead

We had never profiled the query, because the cache made it look fast. When we did, about 70% of its time went to an aggregate over `usage_events` computed at read time.

We made three changes:

- **Counter columns:** we replaced the aggregate with counters on the account row, updated in the same transaction as the event insert.
- **Covering index:** we added one for the most expensive remaining join.
- **Replica routing:** we sent the endpoint to the replicas only.

Then we disabled the cache behind a flag for 5% of traffic, then 50%, then all of it.

| | p50 | p99 |
|---|---|---|
| Before cache | 6 ms | 41 ms |
| With cache | 1.8 ms | 67 ms |
| No cache, fixed query | 3.1 ms | 19 ms |

The change had costs. p50 is 1.3 ms worse than it was with the cache. Peak replica CPU went from 22% to 35%. Event inserts now take a row lock on the account, which we are watching for our highest-volume customers.

In exchange, we deleted about 1,100 lines of invalidation code and dropped a dependency from the on-call rotation. The two stale-data incidents we had over the summer can't recur.

The counter columns are also a cache. The difference is that they live in the same database as the data they summarize and change in the same transaction, so there is no invalidation to get wrong.

## What we'd tell ourselves in June

- **Measure hit and miss latency separately from day one.** A blended median will always flatter a cache.
- **Work out where your p99 lives.** If your miss rate is above 1% and misses are slower than hits, your p99 is a miss.
- **Profile the query before you cache it.** The cache hid a problem we could have fixed in a week.
- **Look at the full distribution of value sizes.** Our median was 3 KB, and the damage came from the 6 MB values.

A cache earns its place when the query is expensive for every key, the values are small, and the hit rate is high enough that misses fall outside the percentiles you care about. Our endpoint met none of those conditions.

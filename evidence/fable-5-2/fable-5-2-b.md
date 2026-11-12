# Why we removed our cache

In June we put a Redis read-through cache in front of Postgres for our account summary endpoint. In October we removed it. While it ran, median latency fell by two thirds and p99 rose by more than half. This post explains how both happened and what we did instead.

## The setup

`GET /accounts/:id/summary` backs the dashboard every customer sees after login. It joins four tables and aggregates an account's invoices and usage. At peak it serves about 2,400 requests per second. Before the cache, p50 was 6 ms and p99 was 48 ms, and p99 was climbing as our largest accounts grew.

The cache was the standard pattern. Check Redis for `summary:{account_id}` and return it on a hit. On a miss, query Postgres, write the JSON to Redis with a five-minute TTL, and return it. Any write to the underlying tables deleted the key.

## What happened to latency

| Period | p50 | p99 |
|---|---|---|
| Before the cache | 6.0 ms | 48 ms |
| Cache, first month | 1.9 ms | 57 ms |
| Cache, after downsizing Postgres | 1.8 ms | 74 ms |
| Cache removed, query fixed | 4.9 ms | 31 ms |

The hit rate settled at 82%, and for the first few weeks we read that as proof the cache was working.

## Why p99 got worse

**The cache sped up requests that were already fast.** Hits were concentrated in small, active accounts, whose queries took 3 to 5 ms anyway because their rows were already in Postgres's buffer cache. The slow requests came from two groups: long-tail accounts that log in a few times a day, whose keys had always expired, and very large accounts, whose keys were deleted by writes every few seconds. Accounts whose queries took longer than 40 ms had a hit rate of 23%. In traces, 96% of requests slower than 40 ms were misses. So p99 was made of misses, and each miss now did everything it had done before plus a Redis round trip, a JSON serialization, and a write-back.

**Large values delayed small ones.** The largest 1% of summaries serialized to more than 900 KB. Our Redis client multiplexes commands over a few connections per instance, so a reply of that size held up every response queued behind it on the same connection. A GET that normally took 0.4 ms took 5 to 12 ms when it landed behind one. This penalty fell on hits as well as misses.

**We shrank Postgres because of the cache.** The cache cut Postgres read load by about 70%, so in July we moved the read replica from 64 GB of memory to 32 GB. The working set no longer fit in memory, the buffer cache hit ratio dropped from 99.4% to 96.1%, and the misses, which were already the slow requests, started waiting on disk reads. p99 went from 57 ms to 74 ms that week. We had also made Redis a hard dependency: a failover in August emptied the cache, the smaller replica received the full uncached load, and p99 was 1.9 seconds for six minutes.

## Stale data

We had three stale-data incidents in four months, all with the same cause: a new write path changed one of the four tables and didn't delete the key. In the worst one, a customer saw a paid invoice shown as overdue for five minutes. None was severe, but each took about a day to find.

## What we did instead

We removed the cache, moved the replica back to 64 GB, and spent two weeks on the query the cache had let us avoid.

- We added a composite index on `invoices (account_id, status, due_date)`, which turned the most expensive step into an index-only scan.
- We moved usage aggregation into a rollup table, `account_usage_daily`, updated in the same transaction as each usage write. This is also precomputed data, but it can't go stale and it has no miss path.
- We split invoice line-item history into its own paginated endpoint, which took the largest responses from over 900 KB to under 40 KB.

The worst-case query went from about 250 ms to 22 ms, and p99 is now 31 ms. p50 is 4.9 ms, about 3 ms slower than with the cache, which nobody loading a dashboard can perceive.

## What we'd check before adding a cache again

- **Hit rate among slow requests.** Ours was 82% overall and 23% on the slow accounts.
- **The miss path, traced separately.** It has its own latency distribution, and it is where the slow requests are.
- **Whether the database is already caching.** A 99.4% buffer cache hit ratio meant most of our reads were served from memory before Redis was involved.
- **What happens when the cache is empty.** If the database can't carry the full load, the cache is a dependency and has to be operated as one.

A read-through cache would have been the right choice if our expensive queries had been on frequently read, rarely written keys, or if Postgres had been short of CPU. Neither was true for us.

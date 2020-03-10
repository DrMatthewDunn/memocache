# memocache
Python - memoize layer for memcaching.

A simple memoize library to improve speed and reduce memcache hits.

This library was initially developed for use within Google AppEngine.
GAE (Python 2.7) provides a memcache shared between instances.

While it is fast, it is "milliseconds not microseconds."
This common memo-then-cache shim economizes on memcache reads and reduces duplicates.

Extending this to front-end Redis would make a ton of sense.

Utilizes memoization library https://github.com/lonelyenvoy/python-memoization
and ExpiringDict https://pypi.org/project/expiringdict/.



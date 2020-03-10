## -*- coding: utf-8 -*-
from google.appengine.api import memcache
from memoization import cached #https://github.com/lonelyenvoy/python-memoization
from expiringdict import ExpiringDict
from datetime import datetime


#dict of keys that have been memo'd
keycache = ExpiringDict(max_len=1000,max_age_seconds=3600)


@cached(ttl=59)  #set TTL to suit
def memcacheget(key):
    value = memcache.get(key)
    return value


#memoized objects - if not then memcache
class memocache():
    '''
    Cache in memo, then memcache

    Retrieve direct from memo without checking memcache if available
    else return from memcache & stash key in keycache
    '''
   
    def __init__(self):
        pass

    @classmethod
    def get(cls,key):
        '''
        Retrieve from cache; memo first, then memcache, else None.
        '''
        learned = keycache.get(key,None)
        if learned: #key already in memcache so it'll actually retrieve from memo
            value = memcacheget(key)
            return value
        else:  #key not learned or forgotten
            value = memcache.get(key)
            if value:  #in memcache but key unlearned or forgotten
                keycache[key] = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()) #save key with utc timestamp as value just in case
                return value
            else:
                return None

    @classmethod
    def add(cls,key=None,value=None,time=None):
        '''
        Add value to cache, add key to keycache
        '''
        keycache[key] = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()) #add key to dictionary of memo'd keys
        if time:
            memcache.add(key,value,time=time)
        else:
            memcache.add(key,value) #DS record permanent; memo cache still only 59 seconds
        return

    @classmethod
    def delete(cls,key):
        '''
        Remove key from keycache, value from memcache
        '''
        keycache.pop(key)
        memcache.delete(key)

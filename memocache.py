## -*- coding: utf-8 -*-
from google.appengine.api import memcache
from memoization import cached #https://github.com/lonelyenvoy/python-memoization
from expiringdict import ExpiringDict
from datetime import datetime


#dict of keys that have been memo'd
keycache = ExpiringDict(max_len=1000,max_age_seconds=3600)


@cached(ttl=59)  #set TTL to suit
def memcacheget(memkey):
    item = memcache.get(memkey)
    return item


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
    def get(cls,memkey):
        '''
        Retrieve from cache; memo first, then memcache, else None.
        '''
        learned = keycache.get(memkey,None)
        if learned: #key already in memcache so it'll actually retrieve from memo
            item = memcacheget(memkey)
            return item
        else:  #key not learned or forgotten
            item = memcache.get(memkey)
            if item:  #in memcache but key unlearned or forgotten
                keycache[memkey] = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()) #save key with utc timestamp as value just in case
                return item
            else:
                return None

    @classmethod
    def add(cls,memkey,item,time=None):
        '''
        Add item to cache, add key to keycache
        '''
        keycache[memkey] = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()) #add key to dictionary of memo'd keys
        if time:
            memcache.add(memkey,item,time=time)
        else:
            memcache.add(memkey,item) #DS record permanent; memo cache still only 59 seconds
        return

    @classmethod
    def delete(cls,memkey):
        '''
        Remove key from keycache, item from memcache
        '''
        keycache.pop(memkey)
        memcache.delete(memkey)

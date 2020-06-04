## -*- coding: utf-8 -*-
from google.appengine.api import memcache
from memoization import cached #https://github.com/lonelyenvoy/python-memoization
#from expiringdict import ExpiringDict eliminated -- perf was quirky
from datetime import datetime


#dict of keys that have been memo'd
#keycache = ExpiringDict(max_len=1000,max_age_seconds=3600)
keycache = {}

def check_keycache():
    cache_max = 1000
    if len(keycache) > cache_max:
        top = len(keycache) - int(cache_max / 10) #10% padding
        keep = sorted(keycache.values(),reverse=True)[0:top]
        newcache = {key:value for key,value in keycache.iteritems() if value in keep}
        keycache.update(newcache)

@cached(ttl=100,thread_safe=False) 
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
        self.cache_max = 1000
        pass

    @classmethod
    def get(cls,key):
        learned = keycache.get(key,None)
        if learned: #key already in memcache so will actually retrieve from memo
            value = memcacheget(key)
            if not value:
                keycache.pop(key,None)
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
        check_keycache()
        if all([key,value]):
            keycache[key] = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()) #add key to dictionary of memo'd keys
            if time:
                memcache.add(key,value,time=time)
            else:
                memcache.add(key,value) #DS record permanent; memo cache still only 59 seconds
            return True
        else:
            return False


    @classmethod
    def delete(cls,key):
        keycache.pop(key)
        memcache.delete(key)



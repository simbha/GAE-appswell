"""
    Config values for memcache
    
    To use in controller:
    
    import config.cache
    CacheConfig = config.cache.Memcache.get(cache_key, 'default')
"""

Memcache = {
    'memcache_demo' : {
        'duration' : 30
    },
    'default' : {
        'duration' : 60
    }
}

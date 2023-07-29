from django.core.cache import cache
from django.utils.cache import get_cache_key
import logging


logger = logging.getLogger(__name__)

class APICachingMieeldware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == 'GET' or response.status_code == 200:
            # print("request.meta", request.META)
            cache_key = get_cache_key(request,method='GET', key_prefix=None)
            if not cache_key:
                return response
            
            cached_response = cache.get(cache_key)
            if cached_response:
                return cached_response
            
            # if not cached, store the response in cache
            cache.set(cache_key, response, timeout=3600)

        return response
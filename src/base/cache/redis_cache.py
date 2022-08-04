import logging

from django.core.cache import cache

logger = logging.getLogger('django')


def set_cache(key: str, value: str, ttl: int) -> bool:
    try:
        cache.set(key, value, timeout=ttl)
    except Exception as err:
        logger.info(f'cannot set cache data: {err}')
        return False
    return True


def get_cache(key: str) -> bool:
    try:
        return cache.get(key)
    except Exception as err:
        logger.info(f'cannot get cache data: {err}')
        return False


def delete_cache(key: str) -> bool:
    try:
        cache.delete(key)
    except Exception as err:
        logger.info(f'cannot delete cache data: {err}')
        return False
    return True

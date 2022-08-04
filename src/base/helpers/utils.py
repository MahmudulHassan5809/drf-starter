import re
from typing import Callable, List
from django.db.models import Lookup
from django.apps import apps


def create_slug(title: str, random_str: str = None) -> str:
    title = re.sub('[^A-Za-z ]+', ' ', title).lower().strip()
    title = re.sub(' +', '-', title)
    if random_str:
        return title + '-' + random_str
    return title


def entries_to_remove(data: dict, removeable_keys: tuple) -> dict:
    for k in removeable_keys:
        data.pop(k, None)
    return data


def format_filter_string(old_dict, keys):
    filtered_dict = {}
    for k in keys:
        if old_dict.get(k):
            filtered_dict[k] = old_dict.get(k)
    return filtered_dict


def get_model_from_app(app_name: str, model_name: str):
    try:
        return apps.get_model(app_label=app_name, model_name=model_name)
    except Exception as ex:
        return None


def flatten(l_data):
    return [item for sublist in l_data for item in sublist]


def snake_to_title(string: str):
    return string.replace("_", " ").title()


class NotEqual(Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


def remove_duplicate_from_list(iterable: List, key:  Callable = None) -> List:
    if key is None:
        def key(x): return x

    seen = set()
    for elem in iterable:
        k = key(elem)
        if k in seen:
            continue

        yield elem
        seen.add(k)

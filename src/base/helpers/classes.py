import json
from datetime import date, datetime, time


class DTEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is datetime object
        # convert it to a string
        if isinstance(obj, datetime):
            return str(obj)
        if isinstance(obj, date):
            return str(obj)
        if isinstance(obj, time):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)
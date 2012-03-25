from datetime import datetime
import simplejson

class FlaskupJSONEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return super(self, obj)


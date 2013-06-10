from datetime import date, datetime
import simplejson


class date_encoder(simplejson.JSONEncoder):
    """
    Encode a datetime.date object in ISO 8601 format.

    http://simplejson.readthedocs.org/en/latest/index.html#simplejson.JSONEncoder
    """
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        else:
            return super(self, obj)


def date_decoder(d):
    """
    Decode a date in ISO 8601 format to a datetime.date object.

    http://simplejson.readthedocs.org/en/latest/index.html#simplejson.JSONDecoder
    """
    if isinstance(d, list):
        pairs = enumerate(d)
    elif isinstance(d, dict):
        pairs = d.items()
    result = []
    for k, v in pairs:
        if isinstance(v, basestring):
            try:
                v = datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                pass
        elif isinstance(v, (dict, list)):
            v = date_decoder(v)
        result.append((k, v))
    if isinstance(d, list):
        return [x[1] for x in result]
    elif isinstance(d, dict):
        return dict(result)

import urllib


def decode_dict(body_dict):
    return {key: str(value) for key, value in body_dict.items()}

def parse_objects_for_json_react(body):
    """
    For 'react'
    """
    return decode_dict(body)

def parse_objects_for_json_requests(body):
    """
    For 'requests' library
    """
    if isinstance(body, dict):
        return decode_dict(body)
    else:
        body = urllib.parse.unquote_plus(body)
        fields = body.split("&")
        fields_dict = {}
        for field in fields:
            att, val = field.split("=")               
            fields_dict[att] = val

        return fields_dict

def parse_objects_to_json(body, *, source='requests'):
    """
        Mainly used to take inputs in the form of objects to format it into dict

        + Inputs (utf-8 decoded string or bytes):
            - att1=value1&att2=value2&att3=value3
            - b'username=evvv&email=evram%40evram.com&pass=dy%24e%248Uz&bdate=1996-12-31T20%3A20%3A13.000000'

        + Outputs:
            {
                att1:value1,
                att2:value2,
                att3:value3
            }

        NOTE:
        Different interfaces send different format of requests, for instance using `requests` library in python, sends requests in objects,
        while react interface sends them in different manner, so you as a developer, need to comment/uncomment these two modes.
    """

    if source == 'react':
        return parse_objects_for_json_react(body)
    elif source == 'requests':
        return parse_objects_for_json_requests(body)

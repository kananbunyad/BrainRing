import json
import re
import uuid


async def is_valid_url(url):
    pattern = r"https://3sual\.az/package/\d+"

    return re.match(pattern, url) is not None


async def is_not_link(message):
    regex = r'^(?!.*(?:https?|ftp)://)[^\s]*$'
    return re.match(regex, message) is not None


async def generate_uuid():
    return uuid.uuid4().hex

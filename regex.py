import json
import re


async def is_valid_url(url):
    pattern = r"https://3sual\.az/package/\d+"

    return re.match(pattern, url) is not None


async def is_not_link(message):
    regex = r'^(?!.*(?:https?|ftp)://)[^\s]*$'
    return re.match(regex, message) is not None

#
# async def read_json_file(json_filename):
#     with open(json_filename, "r", encoding="utf-8") as json_file:
#         data = json.load(json_file)
#     return data

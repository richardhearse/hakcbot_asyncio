#!/usr/bin/env python3

import re

from enum import Enum
from collections import namedtuple

NULL = (None, None)
USER_TUPLE = namedtuple('user', 'name bcast mod sub vip permit timestamp')

class AA(Enum):
    ERROR  = 0
    ACCEPT = 1
    DROP   = 2

class AK(Enum):
    DEL = 0
    ADD = 1
    MOD = 2
    EXIST = -1

SUB = re.compile(r'subscriber=(.*?);')
VIP = re.compile(r'vip/1')
MOD = re.compile(r'mod=(.*?);')
USER_TAGS = re.compile(r'@badge-info=(.*?)user-type=')
MESSAGE   = re.compile(r'user-type=(.*)')
TITLE = re.compile(r'(?P<quote>[\'"]).*?(?P=quote)')


VALID_CMD = re.compile(r'(.*?)\((.*?)\)')
CMD = re.compile(r'(.*?)\(')
ARG = re.compile(r'\((.*?)\)')

URL = re.compile(
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z]{2,}\.?)|' # Domain
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # IP Address
    r'(?::\d+)?' # Optional Port eg :8080
    r'(?:/?|[/?]\S+)',
    re.IGNORECASE) # Sepcific pages in url eg /homepage

# TITLE     = re.compile(r'title\((.*?)\)')
# YOUR_MOM  = re.compile(r'yourmom\((.*?)\)')
# YOUR_MUM  = re.compile(r'yourmum\((.*?)\)')
# FLAG      = re.compile(r'flag\((.*?)\)')
# UNFLAG    = re.compile(r'unflag\((.*?)\)')
# PRAISE    = re.compile(r'praise\((.*?)\)')
# QUOTE     = re.compile(r'quote\((.*?)\)')
# QUOTE_ADD = re.compile(r'quoteadd\((.*?),(.*?)\)')

# GIVE_ENTER  = re.compile(r'enter\((.*?)\)')
# GIVE_STATUS = re.compile(r'status\((.*?)\)')



# AA_WL  = re.compile(r'aa_wl\((.*?)\)')
# ADD_WL = re.compile(r'add_wl\((.*?)\)')
# DEL_WL = re.compile(r'del_wl\((.*?)\)')
# PERMIT = re.compile(r'permit\((.*?)\)')

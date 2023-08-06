#coding:utf-8

import uuid
import random
import math
from datetime import datetime


def gen_uuid():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    return suid

def gen_date_str(sep='std'):
    '''
    if sep is std return %Y-%m-%d %H:%M:%S  '2020-06-28 21:26:47'
    if sep is None return %Y%m%d%H%M%S '20200628212651'
    '''
    if sep == 'std':
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif sep == None:
        return datetime.now().strftime("%Y%m%d%H%M%S")
    else:
        raise Exception('sep not definded.')

def gen_phone():
    prefixArray = ["139","138","137","136","135","134","159","158","157","150","151","152","188","187","182","183","184","178","130","131","132","156","155","186","185","176","133","153","189","180","181","177"]
    prefix = random.choice(prefixArray)
    phone = prefix+str(math.floor(random.random()*100000000))
    return phone



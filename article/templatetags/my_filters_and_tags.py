from django import template
from django.utils import timezone
import math, datetime

register = template.Library()

@register.filter(name='transfer')
def transfer(value, arg):
    """ 将输出强制转换为字符串 arg """
    return arg


@register.filter()
def lower(value):
    """ 将字符串转换为小写字符 """
    return value.lower()


@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds <= 60:
        return '刚刚'

    if diff.days == 0 and diff.seconds >= 60 and diff.seconds <= 3600:
        return str(math.floor(diff.seconds / 60)) + '分钟前'

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds <= 86400:
        return str(math.floor(diff.seconds / 3600)) + '小时前'

    if diff.days >= 1 and diff.days <= 30:
        return str(diff.days) + '天前'

    if diff.days >= 30 and diff.days <= 365:
        return str(math.floor(diff.days / 30)) + '个月前'

    if diff.days >= 365:
        return str(math.floor(diff.days / 365)) + '年前'

@register.simple_tag
def currrent_time(format_string):
    return datetime.datetimee.now().strftime(format_string)

@register.simple_tag
def change_http_to_https(url):
    new_url = url.replace('http://', 'https://')
    return new_url
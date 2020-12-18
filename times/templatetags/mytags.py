from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from ..markdown import markdown
from datetime import timedelta
from django.utils import timezone
import re, math

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def markdown2html(value):
    html = markdown(value, with_toc=True)
    matches = re.finditer(r"(<h([0-6])>)", html)
    min_num = 10
    for match in matches:
        if int(match.group(2)) < min_num:
            min_num = int(match.group(2))

    matches = re.finditer(r"(<h([0-6])>|</h([0-6])>)", html)
    if min_num == 1:
        for match in matches:
            num = int(match.group(2) if match.group(2) else match.group(3))
            html = html[:match.end() - 2] + str(num + 2) + html[match.end() - 1:]
    if min_num == 2:
        for match in matches:
            num = int(match.group(2) if match.group(2) else match.group(3))
            html = html[:match.end() - 2] + str(num + 1) + html[match.end() - 1:]
    return mark_safe(html)


@register.simple_tag()
def article_url(page, article, keys):
    return article.get_url(page, keys)


@register.filter()
def relativetime(time):
    time = timezone.localtime(time)
    day = time.date()
    now = timezone.localtime()
    today = now.date()
    if time > now - timedelta(minutes=10):
        return str(int((now - time).total_seconds()) // 60) + "分前"
    if time > now - timedelta(minutes=30):
        return str(int(math.floor((now - time).total_seconds() // 60 * 0.2) / 0.2)) + "分前"
    if time > now - timedelta(minutes=60):
        return str(math.floor((now - time).total_seconds() // 60 / 10) * 10) + "分前"
    if time > now - timedelta(hours=7):
        return str(int((now - time).total_seconds()) // 60 // 60) + "時間前"
    if day == today:
        return "きょう"
    if day == today - timedelta(days=1):
        return "きのう"
    if day > today - timedelta(days=14):
        return str((today - day).days) + "日前"
    if day.year == today.year:
        return time.strftime("%m月%d日")
    return time.strftime("%Y年%m月%d日")
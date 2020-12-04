from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from ..markdown import markdown
import re

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

import re

from django import template
from django.utils.html import format_html, format_html_join

register = template.Library()


@register.filter
def format_article_content(value):
    text = str(value or '').strip()
    if not text:
        return ''

    blocks = re.split(r'\n\s*\n', text)
    rendered_blocks = []

    for block in blocks:
        lines = block.splitlines()
        heading = re.fullmatch(r'(#{2,3})\s+(.+)', lines[0]) if len(lines) == 1 else None
        if heading:
            tag = 'h2' if len(heading.group(1)) == 2 else 'h3'
            rendered_blocks.append(format_html('<{0}>{1}</{0}>', tag, heading.group(2)))
            continue

        paragraph = format_html_join(
            '<br>',
            '{}',
            ((line,) for line in lines),
        )
        rendered_blocks.append(format_html('<p>{}</p>', paragraph))

    return format_html_join('', '{}', ((block,) for block in rendered_blocks))

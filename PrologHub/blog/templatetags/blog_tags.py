from django import template
from blog.models import BlogCategory, Tag

register = template.Library()

@register.inclusion_tag('blog/tags/categories.html', takes_context=True)
def categories(context):
    return dict(
        categories=BlogCategory.objects.all(),
        request=context['request']
    )


@register.inclusion_tag('blog/tags/tags.html', takes_context=True)
def tags(context):
    return dict(
        tags=Tag.objects.all(),
        request=context['request']
    )

from django import template

from organization.models import Organization

register = template.Library()


@register.inclusion_tag('tags/organization.html', takes_context=True)
def organizations(context):
    return {
        'organizations': Organization.objects.all(),
        'request': context['request'],
    }

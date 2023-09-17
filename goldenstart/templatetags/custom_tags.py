from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
import os

register = template.Library()

@register.filter
def filenameWithoutType(value):
    return os.path.basename(value.file.name)

@register.filter
def filename(value):
    return os.path.basename(value.file.name)
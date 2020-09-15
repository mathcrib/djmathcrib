from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def addsuffix(field, suffix):
    return field.label_tag(label_suffix=suffix)

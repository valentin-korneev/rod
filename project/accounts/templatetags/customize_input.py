from django import template


register = template.Library()


@register.filter
def set_attrs(field, attrs):
    custom_attrs = {
        'class': field.css_classes()
    }

    for attr in attrs.split('|'):
        key, value = attr.split('=')
        if key == 'class':
            custom_attrs['class'] += f' {value}'
        else:
            custom_attrs[key] = value

    return field.as_widget(attrs=custom_attrs)


@register.filter
def add_str(str1, str2):
    return str1 + str(str2)

from django import template
#from base.models import Post
register = template.Library()

@register.filter
def add_class(field, class_name):
    """
    Adds a class to a field.
    """
    return field.as_widget(
        attrs={
            'class':' '.join((field.css_classes(), class_name))
        }
    )

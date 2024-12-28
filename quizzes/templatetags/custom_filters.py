from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Retrieve a value from a dictionary using the provided key.
    """
    try:
        return dictionary.get(key, "No Data")
    except AttributeError:
        return "No Data"

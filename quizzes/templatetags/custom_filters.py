from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    """Safely get a value from a dictionary by key."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, None)
    return None


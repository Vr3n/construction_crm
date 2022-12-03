from django import template
from django.urls import resolve
import pdb

register = template.Library()


class ActiveUrlNode(template.Node):
    """
    Simple tag to check which page we are on, based on resolve:
    useful to add an 'active' css class in menu items,
    that needs to be aware when they are selected.
    """

    def __init__(self, request, names, return_value="active"):
        self.request = template.Variable(request)
        self.names = [template.Variable(n) for n in names]
        self.return_values = template.Variable(return_value)

    def render(self, context):
        request = self.request.resolve(context)
        any_of = False

        try:
            url=resolve(request.path_info)
            url_name="%s" % (url.url_name)
            for n in self.names:
                name=n.resolve(context)
                if url_name.startswith(name):
                    any_of=True
                    break
        except:
            print(f"Cannot resolve {request.path_info}")
        return self.return_values if any_of else ''


@register.tag
def active(parser, token):
    """
        Simple tag to check which page we are on, based on resolve;
        Useful to add an 'active' css class in menu items that needs to be
        aware when they are selected.

        Usage:

            {% active request "base:index" %}
            {% active request "base:index" "base:my_view" %}
    """

    try:
        args=token.split_contents()
        return ActiveUrlNode(args[1], args[2:])
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{token.contents.split()[0]} tag requires atleast 2 arguments")

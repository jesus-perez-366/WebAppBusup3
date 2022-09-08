from flask import current_app

from dominate import tags
from visitor import Visitor
class BootstrapRenderer(Visitor):
    def __init__(self, html5=True, id=None):
        self.html5 = html5
        self._in_dropdown = False
        self.id = id

class Renderer(Visitor):
    """Base interface for navigation renderers.

    Visiting a node should return a string or an object that converts to a
    string containing HTML."""

    def visit_object(self, node):
        """Fallback rendering for objects.

        If the current application is in debug-mode
        (``flask.current_app.debug`` is ``True``), an ``<!-- HTML comment
        -->`` will be rendered, indicating which class is missing a visitation
        function.

        Outside of debug-mode, returns an empty string.
        """
        if current_app.debug:
            return tags.comment('no implementation in {} to render {}'.format(
                self.__class__.__name__,
                node.__class__.__name__, ))
        return ''


class SimpleRenderer(Renderer):
    """A very basic HTML5 renderer.

    Renders a navigational structure using ``<nav>`` and ``<ul>`` tags that
    can be styled using modern CSS.

    :param kwargs: Additional attributes to pass on to the root ``<nav>``-tag.
    """

    def __init__(self, html5=True, id=None,**kwargs):
        self.kwargs = kwargs
        self._in_dropdown = False
        self.id = id
        self.html5 = html5

    def visit_Link(self, node):
        return tags.a(node.text, href=node.get_url())

    def visit_Navbar(self, node):
        kwargs = {'_class': 'navbar'}
        kwargs.update(self.kwargs)

        cont = tags.nav(**kwargs)
        ul = cont.add(tags.ul())

        for item in node.items:
            ul.add(tags.li(self.visit(item)))

        return cont

    def visit_View(self, node):
        kwargs = {}
        if node.active:
            kwargs['_class'] = 'active'
        return tags.a(node.text,
                      href=node.get_url(),
                      title=node.text,
                      **kwargs)

    def visit_Subgroup(self, node):
        if not self._in_dropdown:
            li = tags.li(_class='dropdown')
            if node.active:
                li['class'] = 'active'
            a = li.add(tags.a(node.title, href='#', _class='dropdown-toggle'))
            a['data-toggle'] = 'dropdown'
            a['type'] = 'button'
            a['aria-haspopup'] = 'true'
            a['aria-expanded'] = 'false'
            a.add(tags.span(_class='caret'))

            ul = li.add(tags.ul(_class='dropdown'))

            self._in_dropdown = True
            for item in node.items:
                ul.add(self.visit(item))
            self._in_dropdown = False

            return li
        else:
            raise RuntimeError('Cannot render nested Subgroups')

    def visit_Separator(self, node):
        return tags.hr(_class='separator')

    def visit_Text(self, node):
        return tags.span(node.text, _class='nav-label')

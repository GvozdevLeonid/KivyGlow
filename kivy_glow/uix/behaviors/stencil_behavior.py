__all__ = ('StencilBehavior', )

from kivy.lang import Builder
from kivy.properties import VariableListProperty

Builder.load_string(
    '''
<StencilBehavior>
    canvas.before:
        StencilPush
        RoundedRectangle:
            radius: root.radius if root.radius else (0, 0, 0, 0)
            size: root.size
            pos: root.pos
        StencilUse
    canvas.after:
        StencilUnUse
        RoundedRectangle:
            radius: root.radius if root.radius else (0, 0, 0, 0)
            size: root.size
            pos: root.pos
        StencilPop
''',
)


class StencilBehavior:
    '''
    Stencil behavior class.
    '''

    radius = VariableListProperty([0], length=4)
    '''Canvas radius.

    :attr:`radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `(0, 0, 0, 0)`.
    '''

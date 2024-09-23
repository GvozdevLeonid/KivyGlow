__all__ = ('StencilBehavior', )

from kivy.properties import VariableListProperty
from kivy.lang import Builder


Builder.load_string(
    '''
<StencilBehavior>
    canvas.before:
        StencilPush
        RoundedRectangle:
            pos: root.pos
            size: root.size
            radius: root.radius if root.radius else [0, 0, 0, 0]
        StencilUse
    canvas.after:
        StencilUnUse
        RoundedRectangle:
            pos: root.pos
            size: root.size
            radius: root.radius if root.radius else [0, 0, 0, 0]
        StencilPop
'''
)


class StencilBehavior:
    '''
    Stencil behavior class.
    '''

    radius = VariableListProperty([0], length=4)
    '''Canvas radius.

    :attr:`radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`.
    '''

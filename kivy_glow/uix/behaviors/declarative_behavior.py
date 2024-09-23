'''
DeclarativeBehavior was written by Andrés Rodríguez, Ivanov Yuri, Artem Bulgakov and KivyMD contributors.
https://github.com/kivymd/KivyMD
'''
__all__ = ('DeclarativeBehavior', )

from kivy.properties import StringProperty
from kivy.uix.widget import Widget


class DeclarativeBehavior:
    '''
    Declarative behavior class.

    Allow  you to write Python code in a declarative style.
    '''

    id = StringProperty(None, allownone=True)
    '''Widget id

    :attr:`id` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    '''

    def __init__(self, *args, **kwargs) -> None:
        supported_keys = list(self.properties().keys()) + ['__no_builder']
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in supported_keys or k.startswith('on_')}
        super().__init__(*args, **filtered_kwargs)

        for key, value in kwargs.items():
            if key not in filtered_kwargs.keys():
                setattr(self, key, value)

        for child in args:
            if issubclass(child.__class__, Widget):
                self.add_widget(child)

                if hasattr(child, 'id') and child.id:
                    self.ids[child.id] = child

                for child_id, sub_child in child.ids.items():
                    if child_id not in self.ids.keys():
                        self.ids[child_id] = sub_child

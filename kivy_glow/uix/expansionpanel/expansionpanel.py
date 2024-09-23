__all__ = ('GlowExpansionPanel', )

from kivy_glow.uix.tablelayout import GlowTableLayout
from kivy_glow.uix.boxlayout import GlowBoxLayout
from kivy_glow.uix.button import GlowButton
from kivy_glow.uix.label import GlowLabel
from kivy_glow import kivy_glow_uix_dir
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
import os
from kivy.properties import (
    NumericProperty,
    StringProperty,
    OptionProperty,
    ObjectProperty,
)


with open(
    os.path.join(kivy_glow_uix_dir, 'expansionpanel', 'expansionpanel.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


class GlowExpansionPanelException(Exception):
    pass


class GlowExpansionPanelHeader(GlowBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adaptive_height = True


class GlowExpansionPanel(GlowTableLayout):
    '''Expandable panel.

    This panel has a custom title and can hide or show content when you click on the expand/hide button
    '''

    icon_opened = StringProperty('chevron-up')
    '''Icon for opened state

    :attr:`icon_opened` is an :class:`~kivy.properties.StringProperty`
    and defaults to `chevron-up`.
    '''

    icon_closed = StringProperty('chevron-down')
    '''Icon for closed state

    :attr:`icon_closed` is an :class:`~kivy.properties.StringProperty`
    and defaults to `chevron-down`.
    '''

    header = StringProperty('')
    '''Simple text title

    :attr:`header` is an :class:`~kivy.properties.StringProperty`
    and defaults to `empty`.
    '''
    header_content = ObjectProperty(None, allownone=True)
    '''Your custom header content.
    You should inherit your header from GlowExpansionPanelHeader class.

    :attr:`header_content` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    '''

    expandable_content = ObjectProperty(None, allownone=True)
    '''Your expandable content.
    You can use any widget for your content.

    :attr:`expandable_content` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    '''

    state = OptionProperty('closed', options=('opened', 'closed'))
    '''Current panel state

    :attr:`state` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `slosed`.
    '''

    opening_transition = StringProperty('out_cubic')
    '''Transition for opening animation

    :attr:`opening_transition` is an :class:`~kivy.properties.StringProperty`
    and defaults to `out_cubic`.
    '''

    opening_time = NumericProperty(.2)
    '''Diration for opening animation

    :attr:`opening_time` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `.2`.
    '''

    closing_transition = StringProperty('out_sine')
    '''Transition for closing animation

    :attr:`closing_transition` is an :class:`~kivy.properties.StringProperty`
    and defaults to `out_sine`.
    '''

    closing_time = NumericProperty(.2)
    '''Duration for closing animation

    :attr:`closing_time` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `.2`.
    '''

    _anim_playing = False

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.adaptive_height = True

        Clock.schedule_once(self.set_default_colors, -1)
        Clock.schedule_once(self.initialize_expansionpanel, -1)

    def on_open(self) -> None:
        '''Fired at the ExpansionPanel open event.'''
        pass

    def on_dismiss(self) -> None:
        '''Fired at the ExpansionPanel close event.'''
        pass

    def open(self):
        '''Open ExpansionPanel.'''
        if self.state == 'closed' and not self._anim_playing:
            self._anim_playing = True
            self.state = 'opened'
            self.button.icon = self.icon_opened

            self.expandable_content.opacity = 0
            Window.add_widget(self.expandable_content)
            Clock.schedule_once(self._continue_open)

    def dismiss(self):
        '''Close ExpansionPanel.'''
        if self.state == 'opened' and not self._anim_playing:
            self._anim_playing = True
            self.state = 'closed'
            self.button.icon = self.icon_closed

            animation = Animation(
                opacity=0.0,
                d=self.closing_time / 2,
                t=self.closing_transition,
            )
            animation.bind(on_complete=self._clear_container)
            animation.start(self.container)

    def _continue_open(self, *args) -> None:
        '''Continue opening ExpansionPanel.'''
        Window.remove_widget(self.expandable_content)
        self.expandable_content.opacity = 1
        animation = Animation(
            height=self.expandable_content.height,
            d=self.opening_time / 2,
            t=self.opening_transition,
        )
        animation.bind(on_complete=self._fill_container)
        animation.start(self.container)

    def _fill_container(self, *args) -> None:
        '''Continue opening ExpansionPanel.'''
        self.container.add_widget(self.expandable_content)

        animation = Animation(
            opacity=1,
            d=self.opening_time / 2,
            t=self.opening_transition,
        )
        animation.bind(on_complete=self._cancel_anim)
        animation.start(self.container)

    def _clear_container(self, *args) -> None:
        '''Continue closing ExpansionPanel.'''
        self.container.remove_widget(self.expandable_content)
        animation = Animation(
            height=0,
            d=self.closing_time / 2,
            t=self.closing_transition,
        )
        animation.bind(on_complete=self._cancel_anim)
        animation.start(self.container)

    def _cancel_anim(self, *args) -> None:
        '''Final step for closing and oppening.'''
        self._anim_playing = False

    def _change_state(self, button_instance: GlowButton) -> None:
        '''Open or close ExpansionPanel by clicking on button'''
        if self.state == 'closed':
            self.open()
        elif self.state == 'opened':
            self.dismiss()

    def _init_open(self) -> None:
        '''Open ExpansionPanel if :attr:`state` is `opened` on initialization.'''
        self.button.icon = self.icon_opened

        self.expandable_content.opacity = 0
        Window.add_widget(self.expandable_content)
        Clock.schedule_once(self._continue_init_open)

    def _continue_init_open(self, *args) -> None:
        '''Continue opining ExpansionPanel if :attr:`state` is `opened` on initialization.'''
        Window.remove_widget(self.expandable_content)
        self.container.height = self.expandable_content.height
        self.expandable_content.opacity = 1
        self.container.opacity = 1
        self.container.add_widget(self.expandable_content)

    def initialize_expansionpanel(self, *args) -> None:
        '''Initializing the ExpansionPanel.'''
        if len(self.children) == 1:
            self.expandable_content = self.children[0]
            self.remove_widget(self.expandable_content)

        elif len(self.children) == 2:
            if isinstance(self.children[0], GlowExpansionPanelHeader):
                self.header_content = self.children[0]
                self.expandable_content = self.children[1]

                self.remove_widget(self.header_content)
                self.remove_widget(self.expandable_content)
            elif isinstance(self.children[1], GlowExpansionPanelHeader):
                self.header_content = self.children[1]
                self.expandable_content = self.children[0]

                self.remove_widget(self.header_content)
                self.remove_widget(self.expandable_content)
            else:
                raise GlowExpansionPanelException('Expansionpanel must have expandable_content and optionally GlowExpansionPanelHeader. Additional widgets are not allowed')
        else:
            raise GlowExpansionPanelException('Expansionpanel must have expandable_content and optionally GlowExpansionPanelHeader. Additional widgets are not allowed')

        if self.header_content is None:
            self.header_content = GlowLabel(text=self.header, font_style='TitleL', adaptive_height=True, pos_hint={'center_y': 0.5})

        self.button = GlowButton(adaptive_size=True,
                                 icon=self.icon_closed,
                                 mode='outline',
                                 pos_hint={'right': 1, 'center_y': 0.5},
                                 on_release=self._change_state,
                                 hidden=self.hidden)
        self.container = GlowBoxLayout(size_hint=(1, None), opacity=0, height=0)

        self.add_widget(self.header_content, row=0, col=0, colspan=9)
        self.add_widget(self.button, row=0, col=9)
        self.add_widget(self.container, row=1, col=0, colspan=10)

        if self.state == 'opened':
            self._init_open()

    def set_default_colors(self, *args) -> None:
        '''Set defaults colors.'''
        if self.bg_color is None:
            self.bg_color = self.theme_cls.background_dark_color

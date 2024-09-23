from kivy_glow.uix.colorpicker import GlowColorPicker
from kivy_glow.uix.button import GlowButton
from kivy_glow.app import GlowApp
from kivy.lang import Builder


button_kv = '''
GlowBoxLayout:
    orientation: 'vertical'
    GlowLabel:
        text: 'GlowButton: filled, outline, soft, soft-outline, text'
        halign: 'center'
    GlowLabel:
        adaptive_height: True
        text: 'Text with icon in left position.'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        GlowVSpacer
        GlowButton:
            mode: 'filled'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'left'
            on_release:
                self.disabled = True
        GlowVSpacer
        GlowButton:
            mode: 'outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
        GlowVSpacer
        GlowButton:
            mode: 'soft'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
        GlowVSpacer
        GlowButton:
            mode: 'soft-outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
        GlowVSpacer
        GlowButton:
            mode: 'text'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
        GlowVSpacer
    GlowLabel:
        adaptive_height: True
        text: 'Text with icon in right position.'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        GlowVSpacer
        GlowButton:
            mode: 'filled'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'right'
        GlowVSpacer
        GlowButton:
            mode: 'outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'right'
        GlowVSpacer
        GlowButton:
            mode: 'soft'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'right'
        GlowVSpacer
        GlowButton:
            mode: 'soft-outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'right'
        GlowVSpacer
        GlowButton:
            mode: 'text'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'right'
        GlowVSpacer
    GlowLabel:
        adaptive_height: True
        text: 'Text with icon in top position.'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        GlowVSpacer
        GlowButton:
            mode: 'filled'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'top'
        GlowVSpacer
        GlowButton:
            mode: 'outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'top'
        GlowVSpacer
        GlowButton:
            mode: 'soft'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'top'
        GlowVSpacer
        GlowButton:
            mode: 'soft-outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'top'
        GlowVSpacer
        GlowButton:
            mode: 'text'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'top'
        GlowVSpacer
    GlowLabel:
        adaptive_height: True
        text: 'Text with icon in bottom position.'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        GlowVSpacer
        GlowButton:
            mode: 'filled'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'bottom'
        GlowVSpacer
        GlowButton:
            mode: 'outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'bottom'
        GlowVSpacer
        GlowButton:
            mode: 'soft'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'bottom'
        GlowVSpacer
        GlowButton:
            mode: 'soft-outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'bottom'
        GlowVSpacer
        GlowButton:
            mode: 'text'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'bottom'
        GlowVSpacer
    GlowLabel:
        adaptive_height: True
        text: 'Only text'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        GlowVSpacer
        GlowButton:
            mode: 'filled'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
        GlowVSpacer
        GlowButton:
            mode: 'outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
        GlowVSpacer
        GlowButton:
            mode: 'soft'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
        GlowVSpacer
        GlowButton:
            mode: 'soft-outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
        GlowVSpacer
        GlowButton:
            mode: 'text'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
        GlowVSpacer
    GlowLabel:
        adaptive_height: True
        text: 'Only icon'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        GlowVSpacer
        GlowButton:
            mode: 'filled'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: None
            icon: 'android'
            icon_position: 'right'
        GlowVSpacer
        GlowButton:
            mode: 'outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: None
            icon: 'android'
            icon_position: 'right'
        GlowVSpacer
        GlowButton:
            mode: 'soft'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: None
            icon: 'android'
            icon_position: 'right'
        GlowVSpacer
        GlowButton:
            mode: 'soft-outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: None
            icon: 'android'
            icon_position: 'right'
        GlowVSpacer
        GlowButton:
            mode: 'text'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: None
            icon: 'android'
            icon_position: 'right'
        GlowVSpacer
    GlowLabel:
        adaptive_height: True
        text: 'Disabled button'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        GlowVSpacer
        GlowButton:
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: '123'
            icon: 'android'
            disabled: True
        GlowVSpacer
        GlowButton:
            mode: 'outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: None
            icon: 'android'
            disabled: True
        GlowVSpacer
        GlowButton:
            mode: 'soft'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: None
            icon: 'android'
            disabled: True
        GlowVSpacer
        GlowButton:
            mode: 'soft-outline'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: None
            icon: 'android'
            icon_position: 'right'
            disabled: True
        GlowVSpacer
        GlowButton:
            mode: 'text'
            pos_hint: {'center_y': .5}
            adaptive_size: True
            text: 'text'
            icon: 'android'
            icon_position: 'right'
            disabled: True
        GlowVSpacer

'''
checkbox_kv = '''
GlowBoxLayout:
    orientation: 'vertical'
    GlowLabel:
        text: 'GlowCheckbox: inactive, active, disabled, active and disabled'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        adaptive_size: True
        pos_hint: {'center_x': .5}
        GlowCheckbox:
        GlowCheckbox:
            active: True
        GlowCheckbox:
            disabled: True
        GlowCheckbox:
            active: True
            disabled: True
    GlowLabel:
        text: 'Radiobutton: inactive, active, disabled, active and disabled'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        adaptive_size: True
        pos_hint: {'center_x': .5}
        GlowCheckbox:
            group: 'one'
        GlowCheckbox:
            group: 'one'
            active: True
        GlowCheckbox:
            group: 'two'
            disabled: True
        GlowCheckbox:
            group: 'two'
            active: True
            disabled: True
    GlowVSpacer
'''
combobox_kv = '''
GlowBoxLayout:
    orientation: 'vertical'
    GlowLabel:
        text: 'GlowComboBox'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        adaptive_height: True
        pos_hint: {'center_x': .5}
        GlowHSpacer
        GlowComboBox:
            id: combobox_1
            items: ['item_1', 'item_2', 'item_3']
        GlowComboBox:
            id: combobox_2
            items: ['item_1', 'item_2', 'item_3']
        GlowComboBox:
            id: combobox_3
            items: ['item_1', 'item_2', 'item_3']
            direction: 'up'
        GlowComboBox:
            id: combobox_4
            items: ['item_1', 'item_2', 'item_3']
            disabled: True
        GlowHSpacer
    GlowVSpacer
'''
dropdown_kv = '''
GlowBoxLayout:
    orientation: 'vertical'
    GlowLabel:
        text: 'GlowDropDown'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        adaptive_height: True
        pos_hint: {'center_x': .5}
        GlowHSpacer
        GlowDropDown:
            id: dropdown_1
            text: 'click'
            items: ['item_1', 'item_2', 'item_3']
        GlowDropDown:
            id: dropdown_2
            text: 'click'
            items: ['item_1', 'item_2', 'item_3']
        GlowDropDown:
            id: dropdown_3
            text: 'click'
            items: ['item_1', 'item_2', 'item_3']
            direction: 'up'
        GlowDropDown:
            id: dropdown_4
            text: 'click'
            items: ['item_1', 'item_2', 'item_3']
            disabled: True
        GlowHSpacer
    GlowVSpacer
'''
expansion_kv = '''
GlowBoxLayout:
    padding: dp(5)
    orientation: 'vertical'
    GlowLabel:
        text: 'GlowExpansionPanel'
        halign: 'center'
    GlowBoxLayout:
        spacing: '10dp'
        adaptive_height: True
        pos_hint: {'center_x': .5}
        GlowExpansionPanel:
            header: 'Simple text header'
            GlowBoxLayout:
                adaptive_height: True
                spacing: dp(10)
                GlowIcon:
                    icon: 'android'
                    color: self.theme_cls.primary_color
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    icon_size: dp(46)
                GlowBoxLayout:
                    adaptive_height: True
                    orientation: 'vertical'
                    GlowLabel:
                        adaptive_height: True
                        text: 'Example of expansion content first row'
                        font_style: 'BodyL'
                    GlowLabel:
                        adaptive_height: True
                        text: 'second row'
                        font_style: 'LabelM'
        GlowExpansionPanel:
            GlowExpansionPanelHeader:
                adaptive_height: True
                spacing: dp(10)
                GlowIcon:
                    icon: 'android'
                    color: self.theme_cls.primary_color
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    icon_size: dp(46)
                GlowBoxLayout:
                    adaptive_height: True
                    orientation: 'vertical'
                    GlowLabel:
                        adaptive_height: True
                        text: 'Custom header'
                        font_style: 'BodyL'
                    GlowLabel:
                        adaptive_height: True
                        text: 'additional text'
                        font_style: 'LabelM'
            GlowBoxLayout:
                adaptive_height: True
                GlowLabel:
                    text: 'Expansion content'
    GlowVSpacer
    GlowBoxLayout:
        spacing: '10dp'
        adaptive_height: True
        pos_hint: {'center_x': .5}
        GlowExpansionPanel:
            header: 'Simple text header'
            GlowBoxLayout:
                adaptive_height: True
                spacing: dp(10)
                GlowIcon:
                    icon: 'android'
                    color: self.theme_cls.primary_color
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    icon_size: dp(46)
                GlowBoxLayout:
                    adaptive_height: True
                    orientation: 'vertical'
                    GlowLabel:
                        adaptive_height: True
                        text: 'Example of expansion content first row'
                        font_style: 'BodyL'
                    GlowLabel:
                        adaptive_height: True
                        text: 'second row'
                        font_style: 'LabelM'
        GlowExpansionPanel:
            GlowExpansionPanelHeader:
                adaptive_height: True
                spacing: dp(10)
                GlowIcon:
                    icon: 'android'
                    color: self.theme_cls.primary_color
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    icon_size: dp(46)
                GlowBoxLayout:
                    adaptive_height: True
                    orientation: 'vertical'
                    GlowLabel:
                        adaptive_height: True
                        text: 'Custom header'
                        font_style: 'BodyL'
                    GlowLabel:
                        adaptive_height: True
                        text: 'additional text'
                        font_style: 'LabelM'
            GlowBoxLayout:
                adaptive_height: True
                GlowLabel:
                    text: 'Expansion content'
    GlowVSpacer
'''
label_kv = '''
GlowBoxLayout:
    orientation: 'vertical'
    GlowLabel:
        text: 'GlowLabel'
        halign: 'center'
        bg_color: 1, 0, 0, 1
    GlowBoxLayout:
        spacing: '10dp'
        adaptive_height: True
        pos_hint: {'center_x': .5}
        GlowHSpacer
        GlowLabel:
            allow_selection: True
            text: 'This label can be selected'
        GlowLabel:
            allow_selection: True
            widget_style: 'mobile'
            text: 'This label can be selected'
        GlowHSpacer
    GlowScrollView:
        GlowBoxLayout
            orientation: 'vertical'
            adaptive_size: True
            spacing: '10dp'
            GlowLabel:
                font_style: 'DisplayL'
                adaptive_size: True
                text: 'DisplayL\\nDisplayL'
            GlowLabel:
                font_style: 'DisplayM'
                adaptive_size: True
                text: 'DisplayM\\nDisplayM'
            GlowLabel:
                font_style: 'DisplayS'
                adaptive_size: True
                text: 'DisplayS\\nDisplayS'
            GlowLabel:
                font_style: 'HeadlineL'
                adaptive_size: True
                text: 'HeadlineL\\nHeadlineL'
            GlowLabel:
                font_style: 'HeadlineM'
                adaptive_size: True
                text: 'HeadlineM\\nHeadlineM'
            GlowLabel:
                font_style: 'HeadlineS'
                adaptive_size: True
                text: 'HeadlineS\\nHeadlineS'
            GlowLabel:
                font_style: 'TitleL'
                adaptive_size: True
                text: 'TitleL\\nTitleL'
            GlowLabel:
                font_style: 'TitleM'
                adaptive_size: True
                text: 'TitleM\\nTitleM'
            GlowLabel:
                font_style: 'TitleS'
                adaptive_size: True
                text: 'TitleS\\nTitleS'
            GlowLabel:
                font_style: 'BodyL'
                adaptive_size: True
                text: 'BodyL\\nBodyL'
            GlowLabel:
                font_style: 'BodyM'
                adaptive_size: True
                text: 'BodyM\\nBodyM'
            GlowLabel:
                font_style: 'BodyS'
                adaptive_size: True
                text: 'BodyS\\nBodyS'
            GlowLabel:
                font_style: 'LabelL'
                adaptive_size: True
                text: 'LabelL\\nLabelL'
            GlowLabel:
                font_style: 'LabelM'
                adaptive_size: True
                text: 'LabelM\\nLabelM'
            GlowLabel:
                font_style: 'LabelS'
                adaptive_size: True
                text: 'LabelS\\nLabelS'
    GlowVSpacer
'''
list_kv = '''
GlowBoxLayout:
    orientation: 'vertical'
    GlowLabel:
        text: 'GlowList'
        halign: 'center'
    GlowBoxLayout:
        GlowHSpacer
        GlowList:
            viewclass: 'ListItem_1'
            item_properties: ['icon', 'main_text', 'second_text']
            list_data: [('android', 'item_main_text', 'item_second_text') for i in range(20)]
        GlowHSpacer
        GlowList:
            viewclass: 'ListItem_2'
            list_data: ['item_main_text' for i in range(20)]
        GlowHSpacer
    GlowVSpacer
<ListItem_1@GlowSelectableListItem>:
    icon: 'blank'
    main_text: ''
    second_text: ''
    GlowIcon:
        icon: root.icon
        pos_hint: {'center_x': .5, 'center_y': .5}
    GlowBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        GlowLabel:
            adaptive_height: True
            text: root.main_text
            font_style: 'BodyL'
        GlowLabel:
            adaptive_height: True
            text: root.second_text
            font_style: 'LabelM'

<ListItem_2@GlowListItem>:
    text: ' '
    GlowLabel:
        adaptive_height: True
        text: root.text
'''
numberfield_kv = '''
GlowBoxLayout:
    orientation: 'vertical'
    GlowLabel:
        text: 'GlowNumberField'
        halign: 'center'
    GlowBoxLayout:
        GlowHSpacer
        GlowNumberField:
            label: 'Desktop'
            help_text: 'mode:overlap'
        GlowHSpacer
        GlowNumberField:
            number_type: 'float'
            widget_style: 'mobile'
            label: 'Mobile'
            help_text: 'mode:overlap'
        GlowHSpacer
    GlowVSpacer
    GlowBoxLayout:
        GlowHSpacer
        GlowNumberField:
            label: 'Desktop'
            mode: 'inside'
            help_text: 'mode:inside'
        GlowHSpacer
        GlowNumberField:
            number_type: 'float'
            widget_style: 'mobile'
            label: 'Mobile'
            mode: 'inside'
            help_text: 'mode:inside'
        GlowHSpacer
    GlowVSpacer
    GlowBoxLayout:
        GlowHSpacer
        GlowNumberField:
            label: 'Desktop'
            mode: 'outside'
            help_text: 'mode:outside'
        GlowHSpacer
        GlowNumberField:
            number_type: 'float'
            widget_style: 'mobile'
            label: 'Mobile'
            mode: 'outside'
            help_text: 'mode:outside'
        GlowHSpacer
    GlowVSpacer
    GlowBoxLayout:
        GlowHSpacer
        GlowNumberField:
            label: 'Desktop'
            border_style: 'underline'
            help_text: 'border_style:underline'
        GlowHSpacer
        GlowNumberField:
            number_type: 'float'
            widget_style: 'mobile'
            label: 'Mobile'
            border_style: 'underline'
            help_text: 'border_style:underline'
        GlowHSpacer
    GlowVSpacer
'''
panel_kv = '''
GlowBoxLayout:
    orientation: 'vertical'
    GlowLabel:
        text: 'GlowPanel (badge, underline, text)'
        halign: 'center'
    GlowBoxLayout:
        GlowHSpacer
        GlowPanel:
            mode: 'badge'
            tabs: [{'text': f'tab_{i}'} for i in range(3)]
        GlowHSpacer
        GlowPanel:
            mode: 'underline'
            tabs: [{'text': f'tab_{i}'} for i in range(3)]
        GlowHSpacer
        GlowPanel:
            mode: 'text'
            tabs: [{'text': f'tab_{i}'} for i in range(3)]
        GlowHSpacer
    GlowLabel:
        text: 'GlowPanel with many tabs'
        halign: 'center'
    GlowScrollView:
        size_hint_y: None
        height: panel.minimum_height + dp(5)
        do_scroll_y: False
        GlowPanel:
            id: panel
            mode: 'underline'
            adaptive_width: True
            tabs: [{'text': f'tab_{i}'} for i in range(100)]
    GlowVSpacer
'''
toolbar_kv = '''
#: import GlowButton kivy_glow.uix.button.GlowButton
GlowScreen:
    GlowToolBar:
        title: 'Some title'
        pos_hint: {'top': 1}
        left_buttons:
            [
            GlowButton(mode='text', icon='menu', adaptive_size=True, icon_color=self.theme_cls.text_color),
            ]
        right_buttons:
            [
            GlowButton(mode='text', icon='alert', adaptive_size=True, icon_color=self.theme_cls.text_color),
            GlowButton(mode='text', icon='calendar', adaptive_size=True, icon_color=self.theme_cls.text_color),
            GlowButton(mode='text', icon='android', adaptive_size=True, icon_color=self.theme_cls.text_color),
            ]
'''
sidepanel_kv = '''
GlowSidePanelLayout:
    GlowScreenManager:
        id: manager
        GlowScreen:
            name: 'screen_1'
            GlowBoxLayout:
                bg_color: 1, 0, 0, 1
                GlowLabel:
                    text: 'Screen 1'
        GlowScreen:
            name: 'screen_2'
            GlowBoxLayout:
                bg_color: 0, 1, 0, 1
                GlowLabel:
                    text: 'Screen 2'
        GlowScreen:
            name: 'screen_3'
            GlowBoxLayout:
                bg_color: 0, 0, 1, 1
                GlowLabel:
                    text: 'Screen 3'
    GlowSidePanel:
        id: side_panel
        orientation: 'vertical'
        bg_color: self.theme_cls.background_dark_color
        mode: 'overlay'
        GlowSidePanelButton:
            adaptive_height: True
            icon: 'android'
            text: 'button_1'
            selected: True
            on_release:
                manager.current = 'screen_1'
                side_panel.set_state('close') if side_panel.mode != 'embedded' else None
        GlowSidePanelButton:
            adaptive_height: True
            icon: 'android'
            text: 'button_2'
            on_release:
                manager.current = 'screen_2'
                side_panel.set_state('close') if side_panel.mode != 'embedded' else None
        GlowSidePanelButton:
            adaptive_height: True
            icon: 'android'
            text: 'button_3'
            right_text: '+1'
            on_release:
                manager.current = 'screen_3'
                side_panel.set_state('close') if side_panel.mode != 'embedded' else None
        GlowVSpacer
'''

map_kv = '''
GlowBoxLayout:
    padding: '10dp'
    orientation: 'vertical'
    spacing: '10dp'
    GlowRelativeLayout:
        GlowMap:
            size_hint: 1, 1
            id: map_view
            map_source: 'google-hybrid'

'''

text_kv = '''
GlowTableLayout:
    padding: '10dp'
    orientation: 'vertical'
    spacing: '10dp'
    GlowButton:
        adaptive_size: True
        text: '123'
        row: 0
        col: 0
    GlowButton:
        adaptive_size: True
        text: '456789'
        row: 0
        col: 1
    GlowMap:
        row: 1
        col: 0
        colspan: 2
        size_hint: 1, None
        height: dp(500)
        id: map_view
        map_source: 'google-hybrid'

'''

from kivy import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')


def on_button_press(instance):
    print(instance.parent.size, 'press')


def sorting_function(table_data):
    print('sorting_function')
    return zip(
        *sorted(
            enumerate(table_data),
            key=lambda line: line[1][0]
        )
    )


def on_active(table, instance):
    print(instance.parent.parent.idx, instance.active)
    idx = instance.parent.parent.idx
    row_data = table.table_data[idx]
    row_data[3]['active'] = instance.active
    table.update_table_row_data(idx, row_data)


table_data = [((str(i), (1, 0, 0, 1), True), str(100 - i)) for i in range(100)]


if __name__ == '__main__':
    class ExampleApp(GlowApp):
        def build(self):
            # self.theme_cls.theme_style = 'Dark'
            # table = GlowTable(
            #     use_pagination=True,
            #     selectable=True,
            #     columns_info=[
            #         {'name': 'Column 1', 'min_width': 300, 'size_hint': 1},
            #         {'name': 'Column 1', 'min_width': 300, 'size_hint': 1},
            #         {'name': 'Column 1', 'min_width': 300, 'size_hint': 1},
            #     ],
            #     table_data=[(1, 2, 3) for i in range(20)],
            # )

            # self.view = GlowBoxLayout(table, padding=['30dp'])
            self.view = Builder.load_string(button_kv)

            return GlowButton(text='Open', on_release=lambda _: self.open_CP())

        def open_CP(self):
            color_picker = GlowColorPicker(default_color=(1, 0, 1, 1))
            color_picker.bind(on_selected_color=lambda _, color: print(color))
            color_picker.open()

    ExampleApp().run()

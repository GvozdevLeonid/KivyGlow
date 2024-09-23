__all__ = ('GlowFileManager', )

from kivy.uix.modalview import ModalView
from kivy_glow import kivy_glow_uix_dir
from kivy.utils import platform
from kivy.lang import Builder
from typing import Self
import os
import re
from kivy_glow.uix.behaviors import (
    DeclarativeBehavior,
    AdaptiveBehavior,
    StyleBehavior,
    ThemeBehavior,
)
from kivy.properties import (
    BooleanProperty,
    OptionProperty,
    ObjectProperty,
    StringProperty,
    ListProperty,
)

with open(
    os.path.join(kivy_glow_uix_dir, 'filemanager', 'filemanager.kv'), encoding='utf-8'
) as kv_file:
    Builder.load_string(kv_file.read())


extension_to_icon = {
    'doc': 'file-word-outline',
    'docx': 'file-word-outline',
    'mp4': 'file-video-outline',
    'avi': 'file-video-outline',
    'mkv': 'file-video-outline',
    'mov': 'file-video-outline',
    'wmv': 'file-video-outline',

    'xlsx': 'file-excel-outline',
    'xls': 'file-excel-outline',
    'csv': 'file-excel-outline',

    'ppt': 'file-powerpoint-outline',
    'pptx': 'file-powerpoint-outline',

    'pdf': 'file-document-outline',
    'txt': 'file-document-outline',
    'log': 'file-document-outline',
    'rtf': 'file-document-outline',
    'md': 'file-document-outline',

    'html': 'file-code-outline',
    'htm': 'file-code-outline',
    'css': 'file-code-outline',
    'js': 'file-code-outline',
    'ts': 'file-code-outline',
    'json': 'file-code-outline',
    'xml': 'file-code-outline',
    'yaml': 'file-code-outline',
    'yml': 'file-code-outline',
    'py': 'file-code-outline',
    'kv': 'file-code-outline',
    'java': 'file-code-outline',
    'h': 'file-code-outline',
    'c': 'file-code-outline',
    'cpp': 'file-code-outline',
    'cs': 'file-code-outline',
    'rb': 'file-code-outline',
    'php': 'file-code-outline',
    'sh': 'file-code-outline',
    'sql': 'file-code-outline',

    'png': 'file-image-outline',
    'jpg': 'file-image-outline',
    'jpeg': 'file-image-outline',
    'gif': 'file-image-outline',
    'bmp': 'file-image-outline',
    'svg': 'file-image-outline',

    'zip': 'folder-zip-outline',
    'rar': 'folder-zip-outline',
    '7z': 'folder-zip-outline',
    'tar': 'folder-zip-outline',
    'gz': 'folder-zip-outline',

    'mp3': 'file-music-outline',
    'wav': 'file-music-outline',
    'flac': 'file-music-outline',
    'aac': 'file-music-outline',
    'ogg': 'file-music-outline',
    'wma': 'file-music-outline',

    'key': 'file-key-outline',
    'cert': 'file-certificate-outline',
    'p12': 'file-certificate-outline',
    'pfx': 'file-certificate-outline',
    'pem': 'file-certificate-outline',
    'crt': 'file-certificate-outline',
}


class GlowFileManager(DeclarativeBehavior,
                      AdaptiveBehavior,
                      StyleBehavior,
                      ThemeBehavior,
                      ModalView):

    selector = OptionProperty('file', options=['file', 'files', 'folder'])

    ext = ListProperty()

    show_hidden = BooleanProperty(False)

    sort_by = OptionProperty('name', options=['name', 'date', 'size', 'type'], allownone=True)

    sort_reverse = BooleanProperty(False)

    current_path = StringProperty(os.path.expanduser("~"))

    dismiss_manager = ObjectProperty(lambda x: None)
    '''Function called when the user reaches directory tree root or closed manager.

    :attr:`exit_manager` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `lambda x: None`.
    '''

    select_path = ObjectProperty(lambda x: None)
    '''Function, called when selecting a file/directory.

    :attr:`select_path` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `lambda x: None`.
    '''

    _content = ListProperty([])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _back(self, *args):
        path, end = os.path.split(self.current_path)

        if self.current_path and path == self.current_path:
            self.current_path = ''
        else:
            if not end:
                self.dismiss()
            else:
                self.current_path = path

    def dismiss(self) -> None:
        '''Close filefanager.'''
        self.dismiss_manager(self)
        super().dismiss()

    def _select(self):
        if self.selector == 'folder':
            self.select_path(self.current_path)
            self.dismiss()
        elif self.selector == 'files':
            self.select_path([item['path'] for item in self.ids.glow_filemanager_list.selected_items_data])
            self.dismiss()

    def open(self, current_path: str = None) -> None:
        '''Open filemanager with selected path'''

        if current_path is not None:
            self.current_path = current_path
        else:
            self.on_current_path(self, self.current_path)

        super().open()

    def _sort(self, content) -> list[dict]:
        new_content = []
        if self.sort_by is None:
            return content
        elif self.sort_by == 'name':
            new_content = sorted(content, key=lambda obj: obj['display_name'])
        elif self.sort_by == 'date':
            new_content = sorted(content, key=lambda obj: os.path.getctime(obj['path']), reverse=True)
        elif self.sort_by == 'size':
            new_content = sorted(content, key=lambda obj: os.path.getsize(obj['path']), reverse=True)
        elif self.sort_by == 'type':
            new_content = sorted(content, key=lambda obj: obj['display_name'].split('.')[::-1])

        if self.sort_reverse:
            new_content.reverse()

        return new_content

    def on_current_path(self, filemanager_instance: Self, current_path):
        '''Update list view by current_path'''

        new_content = []
        self.ids.glow_filemanager_list.select_all(False)

        if self.selector in ('folder', 'files') and current_path != '':
            self.ids.glow_filemanager_button_select.hidden = False
        else:
            self.ids.glow_filemanager_button_select.hidden = True

        if current_path != '':
            for obj in os.listdir(current_path):
                if os.path.isdir(os.path.join(current_path, obj)):
                    try:
                        obj_in_folder = str(len(os.listdir(os.path.join(current_path, obj))))
                    except Exception:
                        obj_in_folder = ''

                    if obj.startswith("."):
                        if not self.show_hidden:
                            continue
                        else:
                            new_content.append({'is_file': False, 'checkbox_disabled': True, 'obj_in_folder': obj_in_folder, 'icon': 'folder-hidden', 'display_name': obj, 'path': os.path.join(current_path, obj)})
                    else:
                        new_content.append({'is_file': False, 'checkbox_disabled': True, 'obj_in_folder': obj_in_folder, 'icon': 'folder', 'display_name': obj, 'path': os.path.join(current_path, obj)})

                elif self.selector in ('file', 'files'):
                    if len(self.ext) and obj.split('.')[-1].lower() not in self.ext:
                        continue
                    elif obj.startswith("."):
                        if not self.show_hidden:
                            continue
                        else:
                            new_content.append({'is_file': True, 'checkbox_disabled': False, 'obj_in_folder': '', 'icon': 'file-hidden', 'display_name': obj, 'path': os.path.join(current_path, obj)})
                    else:
                        new_content.append({'is_file': True, 'checkbox_disabled': False, 'obj_in_folder': '', 'icon': extension_to_icon.get(obj.split('.')[-1].lower(), 'file-outline'), 'display_name': obj, 'path': os.path.join(current_path, obj)})
        else:
            disks = []
            if platform == "win":
                disks = sorted(
                    re.findall(
                        r"[A-Z]+:.*$",
                        os.popen("mountvol /").read(),
                        re.MULTILINE,
                    )
                )
            elif platform in ["linux", "android"]:
                disks = sorted(
                    re.findall(
                        r"on\s(/.*)\stype",
                        os.popen("mount").read(),
                    )
                )
            elif platform == "macosx":
                disks = sorted(
                    re.findall(
                        r"on\s(/.*)\s\(",
                        os.popen("mount").read(),
                    )
                )
            else:
                return

            for disk in disks:
                new_content.append({'is_file': False, 'icon': 'harddisk', 'display_name': disk, 'path': disk, 'checkbox_disabled': True})

        self._content = self._sort(new_content)

    def on_filemanager_item_press(self, list_instance, file_item_instance):
        if file_item_instance.is_file:
            if self.selector == 'file':
                self.select_path(file_item_instance.path)
                self.dismiss()
        else:
            self.current_path = file_item_instance.path

    def on_filemanager_item_selected(self, list_instance, file_item_instance):
        pass

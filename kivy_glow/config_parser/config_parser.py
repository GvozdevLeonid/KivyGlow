from ast import literal_eval
from collections import OrderedDict
from configparser import RawConfigParser as PythonConfigParser
from os import environ
from typing import (
    Any,
    Callable,
    ClassVar,
)
from weakref import ref

try:
    from kivy.logger import Logger
except ImportError:
    import logging
    Logger = logging.getLogger('ConfigParser')


class ConfigParser(PythonConfigParser):

    def getdefault(self, section: str, option: str, defaultvalue: float | int | str | bool | list | tuple | dict, valuetype: str | None = None) -> float | int | str | bool | list | tuple | dict:
        '''Get the value of an option in the specified section. If not found,
        it will return the default value.
        '''
        if not self.has_section(section) or not self.has_option(section, option):
            return defaultvalue

        valuetype_options: dict[str, Callable] = {
            'int': self.getint,
            'float': self.getfloat,
            'boolean': self.getboolean,
            'list': self.getlist,
            'tuple': self.gettuple,
            'dictionary': self.getdictionary,
        }

        if valuetype in valuetype_options:
            return valuetype_options[valuetype](section, option)

        return self.get(section, option)

    def getdefaultint(self, section: str, option: str, defaultvalue: int) -> int:
        '''Get the value of an option in the specified section. If not found,
        it will return the default value. The value will always be
        returned as an integer.

        '''
        return self.getdefault(section, option, defaultvalue, 'int')

    def getdefaultfloat(self, section: str, option: str, defaultvalue: float) -> float:
        '''Get the value of an option in the specified section. If not found,
        it will return the default value. The value will always be
        returned as an float.

        '''
        return self.getdefault(section, option, defaultvalue, 'float')

    def getdefaultboolean(self, section: str, option: str, defaultvalue: bool) -> bool:
        '''Get the value of an option in the specified section. If not found,
        it will return the default value. The value will always be
        returned as an boolean.

        '''
        return self.getdefault(section, option, defaultvalue, 'boolean')

    def getlist(self, section: str, option: str) -> list:
        return list(literal_eval(self.get(section, option)))

    def getdefaultlist(self, section: str, option: str, defaultvalue: list) -> list:
        '''Get the value of an option in the specified section. If not found,
        it will return the default value. The value will always be
        returned as an list.

        '''
        return self.getdefault(section, option, defaultvalue, 'list')

    def gettuple(self, section: str, option: str) -> tuple:
        return tuple(literal_eval(self.get(section, option)))

    def getdefaulttuple(self, section: str, option: str, defaultvalue: tuple) -> tuple:
        '''Get the value of an option in the specified section. If not found,
        it will return the default value. The value will always be
        returned as an tuple.

        '''
        return self.getdefault(section, option, defaultvalue, 'tuple')

    def getdictionary(self, section: str, option: str) -> dict:
        return dict(literal_eval(self.get(section, option)))

    def getdefaultdictionary(self, section: str, option: str, defaultvalue: dict) -> dict:
        '''Get the value of an option in the specified section. If not found,
        it will return the default value. The value will always be
        returned as an dict.

        '''
        return self.getdefault(section, option, defaultvalue, 'dictionary')


class ExtendedKivyConfigParser(ConfigParser):
    def __init__(self, name: str = '', **kwargs) -> None:
        ConfigParser.__init__(self, **kwargs)
        self._sections: dict = OrderedDict()
        self._callbacks: list = []
        self.filename = None
        self.name = name

    def add_callback(self, callback: Callable, section: str, key: str | None = None) -> None:
        if section is None and key is not None:
            raise Exception('You cannot specify a key without a section')
        self._callbacks.append((callback, section, key))

    def remove_callback(self, callback: Callable, section: str, key: str | None = None) -> None:
        self._callbacks.remove((callback, section, key))

    def _do_callbacks(self, section: str, key: str, value: Any) -> None:
        for callback, csection, ckey in self._callbacks:
            if csection != section:
                continue
            if ckey is not None and ckey != key:
                continue
            callback(section, key, value)

    def read(self, filename: str | None, encoding: str = 'utf-8-sig') -> None:  # type: ignore
        if not isinstance(filename, str):
            raise Exception(f'Only one filename is accepted ({str.__name__})')
        self.filename = filename

        old_vals = {sect: dict(self.items(sect)) for sect in self.sections()}
        ConfigParser.read(self, filename, encoding=encoding)

        f = self._do_callbacks
        for section in self.sections():
            if section not in old_vals:  # new section
                for k, v in self.items(section):
                    f(section, k, v)
                continue

            old_keys = old_vals[section]
            for k, v in self.items(section):
                if k not in old_keys or v != old_keys[k]:
                    f(section, k, v)

    def set(self, section: str, option: str, value: Any) -> None:  # type: ignore
        e_value = value
        if not isinstance(value, str):
            e_value = str(value)
        ConfigParser.set(self, section, option, e_value)
        self._do_callbacks(section, option, value)

    def setall(self, section: str, keyvalues: dict[str, Any]) -> None:
        for key, value in keyvalues.items():
            self.set(section, key, value)

    def get(self, section: str, option: str, **kwargs) -> str:  # type: ignore
        return ConfigParser.get(self, section, option, **kwargs)

    def setdefaults(self, section: str, keyvalues: dict[str, Any]) -> None:
        self.adddefaultsection(section)
        for key, value in keyvalues.items():
            self.setdefault(section, key, value)

    def setdefault(self, section: str, option: str, value: Any) -> None:  # type: ignore
        if self.has_option(section, option):
            return
        self.set(section, option, value)

    def adddefaultsection(self, section: str) -> None:
        '''Add a section if the section is missing.
        '''
        if '_' in section:
            raise ValueError('Section can\'t contain "_" symbol')

        if self.has_section(section):
            return
        self.add_section(section)

    def write(self) -> bool:  # type: ignore
        if self.filename is None:
            return False
        try:
            with open(self.filename, 'w', encoding='utf-8') as fd:
                ConfigParser.write(self, fd)
        except OSError:
            Logger.exception(f'Unable to write the config <{self.filename}>')
            return False
        return True

    def update_config(self, filename: str, overwrite: bool = False) -> None:
        pcp = ConfigParser()
        pcp.read(filename)
        confset = self.setall if overwrite else self.setdefaults
        for section in pcp.sections():
            confset(section, dict(pcp.items(section)))
        self.write()

    @staticmethod
    def _register_named_property(name: str, widget_ref: list, *args) -> None:
        configs = ExtendedKivyConfigParser._named_configs
        try:
            config, props = configs[name]
        except KeyError:
            configs[name] = (None, [widget_ref])
            return

        props.append(widget_ref)
        if config:
            config = config()
        widget = widget_ref[0]()

        if config and widget:  # associate this config with property
            widget.property(widget_ref[1]).set_config(config)

    @staticmethod
    def get_configparser(name: str) -> ConfigParser | None:
        try:
            config = ExtendedKivyConfigParser._named_configs[name][0]
            if config is not None:
                config = config()
                if config is not None:
                    return config

            del ExtendedKivyConfigParser._named_configs[name]
        except KeyError:
            pass
        return None

    _named_configs: ClassVar[dict] = {}
    _name: str = ''

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        old_name = self._name
        if value is old_name:
            return
        self._name = value
        configs = ExtendedKivyConfigParser._named_configs

        if old_name:
            _, props = configs.get(old_name, (None, []))
            for widget, prop in props:
                _widget = widget()
                if _widget:
                    _widget.property(prop).set_config(None)
            configs[old_name] = (None, props)

        if not value:
            return

        try:
            config, props = configs[value]
        except KeyError:
            configs[value] = (ref(self), [])
            return

        if config is not None and config() is not None:
            raise ValueError(f'A parser named {value} already exists')
        for widget, prop in props:
            _widget = widget()
            if _widget:
                _widget.property(prop).set_config(self)
        configs[value] = (ref(self), props)


try:
    import kivy.config
    if not environ.get('KIVY_DOC_INCLUDE'):
        from os.path import exists

        from kivy import kivy_config_fn
        from kivy.logger import logger_config_update
        from kivy.utils import platform

        _is_rpi = exists('/opt/vc/include/bcm_host.h')

        # Version number of current configuration format
        KIVY_CONFIG_VERSION = 27

        kivy.config.Config = ExtendedKivyConfigParser(name='kivy')
        kivy.config.Config.add_callback(logger_config_update, 'kivy', 'log_level')

        # Read config file if exist
        if (exists(kivy_config_fn) and
                'KIVY_USE_DEFAULTCONFIG' not in environ and
                'KIVY_NO_CONFIG' not in environ):
            try:
                kivy.config.Config.read(kivy_config_fn)
            except Exception:
                Logger.exception('Core: error while reading local configuration')

        version = kivy.config.Config.getdefaultint('kivy', 'config_version', 0)

        # Add defaults section
        kivy.config.Config.adddefaultsection('kivy')
        kivy.config.Config.adddefaultsection('graphics')
        kivy.config.Config.adddefaultsection('input')
        kivy.config.Config.adddefaultsection('postproc')
        kivy.config.Config.adddefaultsection('widgets')
        kivy.config.Config.adddefaultsection('modules')
        kivy.config.Config.adddefaultsection('network')

        # Upgrade default configuration until we have the current version
        need_save = False
        if version != KIVY_CONFIG_VERSION and 'KIVY_NO_CONFIG' not in environ:
            Logger.warning(f'Config: Older configuration version detected ({version} instead of {KIVY_CONFIG_VERSION})')
            Logger.warning('Config: Upgrading configuration in progress.')
            need_save = True

        while version < KIVY_CONFIG_VERSION:
            Logger.debug(f'Config: Upgrading from {version} to {version + 1}')

            if version == 0:

                # log level
                kivy.config.Config.setdefault('kivy', 'keyboard_repeat_delay', '300')
                kivy.config.Config.setdefault('kivy', 'keyboard_repeat_rate', '30')
                kivy.config.Config.setdefault('kivy', 'log_dir', 'logs')
                kivy.config.Config.setdefault('kivy', 'log_enable', '1')
                kivy.config.Config.setdefault('kivy', 'log_level', 'info')
                kivy.config.Config.setdefault('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')
                kivy.config.Config.setdefault('kivy', 'window_icon', '')

                # default graphics parameters
                kivy.config.Config.setdefault('graphics', 'display', '-1')
                kivy.config.Config.setdefault('graphics', 'fullscreen', 'no')
                kivy.config.Config.setdefault('graphics', 'height', '600')
                kivy.config.Config.setdefault('graphics', 'left', '0')
                kivy.config.Config.setdefault('graphics', 'maxfps', '0')
                kivy.config.Config.setdefault('graphics', 'multisamples', '2')
                kivy.config.Config.setdefault('graphics', 'position', 'auto')
                kivy.config.Config.setdefault('graphics', 'rotation', '0')
                kivy.config.Config.setdefault('graphics', 'show_cursor', '1')
                kivy.config.Config.setdefault('graphics', 'top', '0')
                kivy.config.Config.setdefault('graphics', 'width', '800')

                # input configuration
                kivy.config.Config.setdefault('input', 'mouse', 'mouse')

                # activate native input provider in configuration
                # from 1.0.9, don't activate mactouch by default, or app are
                # unusable.
                if platform == 'win':
                    kivy.config.Config.setdefault('input', 'wm_touch', 'wm_touch')
                    kivy.config.Config.setdefault('input', 'wm_pen', 'wm_pen')
                elif platform == 'linux':
                    probesysfs = 'probesysfs'
                    if _is_rpi:
                        probesysfs += ',provider=hidinput'
                    kivy.config.Config.setdefault('input', '%(name)s', probesysfs)

                # input postprocessing configuration
                kivy.config.Config.setdefault('postproc', 'double_tap_distance', '20')
                kivy.config.Config.setdefault('postproc', 'double_tap_time', '250')
                kivy.config.Config.setdefault('postproc', 'ignore', '[]')
                kivy.config.Config.setdefault('postproc', 'jitter_distance', '0')
                kivy.config.Config.setdefault('postproc', 'jitter_ignore_devices', 'mouse,mactouch,')
                kivy.config.Config.setdefault('postproc', 'retain_distance', '50')
                kivy.config.Config.setdefault('postproc', 'retain_time', '0')

                # default configuration for keyboard repetition
                kivy.config.Config.setdefault('widgets', 'keyboard_layout', 'qwerty')
                kivy.config.Config.setdefault('widgets', 'keyboard_type', '')
                kivy.config.Config.setdefault('widgets', 'list_friction', '10')
                kivy.config.Config.setdefault('widgets', 'list_friction_bound', '20')
                kivy.config.Config.setdefault('widgets', 'list_trigger_distance', '5')

            elif version == 1:
                kivy.config.Config.set('graphics', 'maxfps', '60')

            elif version == 2:
                # was a version to automatically copy windows icon in the user
                # directory, but it's now not used anymore. User can still change
                # the window icon by touching the config.
                pass

            elif version == 3:
                # add token for scrollview
                kivy.config.Config.setdefault('widgets', 'scroll_timeout', '55')
                kivy.config.Config.setdefault('widgets', 'scroll_distance', '20')
                kivy.config.Config.setdefault('widgets', 'scroll_friction', '1.')

                # remove old list_* token
                kivy.config.Config.remove_option('widgets', 'list_friction')
                kivy.config.Config.remove_option('widgets', 'list_friction_bound')
                kivy.config.Config.remove_option('widgets', 'list_trigger_distance')

            elif version == 4:
                kivy.config.Config.remove_option('widgets', 'keyboard_type')
                kivy.config.Config.remove_option('widgets', 'keyboard_layout')

                # add keyboard token
                kivy.config.Config.setdefault('kivy', 'keyboard_mode', '')
                kivy.config.Config.setdefault('kivy', 'keyboard_layout', 'qwerty')

            elif version == 5:
                kivy.config.Config.setdefault('graphics', 'resizable', '1')

            elif version == 6:
                # if the timeout is still the default value, change it
                kivy.config.Config.setdefault('widgets', 'scroll_stoptime', '300')
                kivy.config.Config.setdefault('widgets', 'scroll_moves', '5')

            elif version == 7:
                # desktop bool indicating whether to use desktop specific features
                is_desktop = int(platform in {'win', 'macosx', 'linux'})
                kivy.config.Config.setdefault('kivy', 'desktop', is_desktop)
                kivy.config.Config.setdefault('postproc', 'triple_tap_distance', '20')
                kivy.config.Config.setdefault('postproc', 'triple_tap_time', '375')

            elif version == 8:
                if kivy.config.Config.getint('widgets', 'scroll_timeout') == 55:
                    kivy.config.Config.set('widgets', 'scroll_timeout', '250')

            elif version == 9:
                kivy.config.Config.setdefault('kivy', 'exit_on_escape', '1')

            elif version == 10:
                kivy.config.Config.set('graphics', 'fullscreen', '0')
                kivy.config.Config.setdefault('graphics', 'borderless', '0')

            elif version == 11:
                kivy.config.Config.setdefault('kivy', 'pause_on_minimize', '0')

            elif version == 12:
                kivy.config.Config.setdefault('graphics', 'window_state', 'visible')

            elif version == 13:
                kivy.config.Config.setdefault('graphics', 'minimum_width', '0')
                kivy.config.Config.setdefault('graphics', 'minimum_height', '0')

            elif version == 14:
                kivy.config.Config.setdefault('graphics', 'min_state_time', '.035')

            elif version == 15:
                kivy.config.Config.setdefault('kivy', 'kivy_clock', 'default')

            elif version == 16:
                kivy.config.Config.setdefault('kivy', 'default_font', [
                    'Roboto',
                    'data/fonts/Roboto-Regular.ttf',
                    'data/fonts/Roboto-Italic.ttf',
                    'data/fonts/Roboto-Bold.ttf',
                    'data/fonts/Roboto-BoldItalic.ttf'])

            elif version == 17:
                kivy.config.Config.setdefault('graphics', 'allow_screensaver', '1')

            elif version == 18:
                kivy.config.Config.setdefault('kivy', 'log_maxfiles', '100')

            elif version == 19:
                kivy.config.Config.setdefault('graphics', 'shaped', '0')
                kivy.config.Config.setdefault(
                    'kivy', 'window_shape',
                    'data/images/defaultshape.png',
                )

            elif version == 20:
                kivy.config.Config.setdefault('network', 'useragent', 'curl')

            elif version == 21:
                kivy.config.Config.setdefault('graphics', 'vsync', '')

            elif version == 22:
                kivy.config.Config.setdefault('graphics', 'verify_gl_main_thread', '1')

            elif version == 23:
                kivy.config.Config.setdefault('graphics', 'custom_titlebar', '0')
                kivy.config.Config.setdefault('graphics', 'custom_titlebar_border', '5')

            elif version == 24:
                kivy.config.Config.setdefault("network", "implementation", "default")

            elif version == 25:
                kivy.config.Config.setdefault('graphics', 'always_on_top', '0')

            elif version == 26:
                kivy.config.Config.setdefault("graphics", "show_taskbar_icon", "1")

            # WARNING: When adding a new version migration here,
            # don't forget to increment KIVY_CONFIG_VERSION !
            else:
                # for future.
                break

            # Pass to the next version
            version += 1

        # Indicate to the Config that we've upgrade to the latest version.
        kivy.config.Config.set('kivy', 'config_version', KIVY_CONFIG_VERSION)

        # Now, activate log file
        Logger.logfile_activated = bool(kivy.config.Config.getint('kivy', 'log_enable'))

        # If no configuration exist, write the default one.
        if ((not exists(kivy_config_fn) or need_save) and
                'KIVY_NO_CONFIG' not in environ):
            try:
                kivy.config.Config.filename = kivy_config_fn
                kivy.config.Config.write()
            except Exception:
                Logger.exception('Core: Error while saving default config file')

        # Load configuration from env
        if environ.get('KIVY_NO_ENV_CONFIG', '0') != '1':
            for key, value in environ.items():
                if not key.startswith("KCFG_"):
                    continue
                try:
                    _, section, name = key.split("_", 2)
                except ValueError:
                    Logger.warning(f"Config: Environ `{key}` invalid format, must be KCFG_section_name")
                    continue

                # extract and check section
                section = section.lower()
                if not kivy.config.Config.has_section(section):
                    Logger.warning(f"Config: Environ `{key}`: unknown section `{section}`")
                    continue

                # extract and check the option name
                name = name.lower()
                sections_to_check = {
                    "kivy", "graphics", "widgets", "postproc", "network"}
                if (section in sections_to_check and
                        not kivy.config.Config.has_option(section, name)):
                    Logger.warning(f"Config: Environ `{key}` unknown `{name}` option in `{section}` section.")
                    # we don't avoid to set an unknown option, because maybe
                    # an external modules or widgets (in garden?) may want to
                    # save its own configuration here.

                kivy.config.Config.set(section, name, value)
except Exception:
    pass

import re

import sublime
from sublime_plugin import TextCommand, EventListener


SETTINGS_REGEX = r'(?:sublimeconf):\s+filetype=([\w][-\w\./\+#]+)'


def get_settings():
    filename = __name__.split('.')[-1] + '.sublime-settings'
    return sublime.load_settings(filename)


def get_setting(name, default=None):
    return get_settings().get(name, default)


def parse_filetype(view):
    # find the region for the first filetype conf snippet
    region = view.find(SETTINGS_REGEX, 0)
    # if there is one, extract the filetype value from the snippet
    match = re.match(SETTINGS_REGEX, view.substr(region))
    return match.group(1) if match else None


def filetype_to_package(filetype):
    """
    Convert a filetype like 'python' to a package path like
    'Packages/Python/Python.tmLanguage", by checking first the
    'user_filetype_package_map' setting, and if not found there,
    returning the mapping in 'default_filetype_package_map' if
    there is one, and falling back to returning the 'filetype' itself,
    which allows the user to specify a package path inline in the file
    if they don't want to define a custom mapping in the settings file.
    """
    user_map = get_setting('user_filetype_package_map') or {}
    default_map = get_setting('default_filetype_package_map') or {}
    package = user_map.get(filetype, default_map.get(filetype, None))
    return package or filetype


def update_filetype(view, filetype):
    new_filetype_path = filetype_to_package(filetype)
    # only set the syntax if it would change it from the current syntax
    curr_filetype_path = view.settings().get('syntax')
    if new_filetype_path and new_filetype_path != curr_filetype_path:
        view.set_syntax_file(new_filetype_path)


def process_view_filetype(view):
    filetype = parse_filetype(view)
    if filetype:
        update_filetype(view, filetype)


class DetectFiletypeCommand(TextCommand):

    def run(self, edit):
        process_view_filetype(self.view)


class DetectFiletypeEventListener(EventListener):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_load(self, view):
        process_view_filetype(view)

    def on_post_save(self, view):
        if get_setting('on_post_save'):
            process_view_filetype(view)


# sublimeconf: filetype=python

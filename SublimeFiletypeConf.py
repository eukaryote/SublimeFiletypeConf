import re

import sublime
from sublime_plugin import TextCommand, EventListener


def load_settings():
    filename = __name__.split('.')[-1] + '.sublime-settings'
    return sublime.load_settings(filename)


def get_setting(name, default=None):
    return load_settings().get(name, default)


def parse_filetype(view):
    """
    Parse the filetype from the given view, returning 'None' if no filetype
    could be identified, or else the filetype string that still needs to
    be resolved from something like 'python' to the form that SublimeText
    needs it in, which is something like 'Packages/Python/Python.tmLanguage'.
    """
    snippet_regex = get_setting('snippet_regex')
    # find the region for the first filetype conf snippet
    region = view.find(snippet_regex, 0)
    # if there is one, extract the filetype value from the snippet
    match = re.match(snippet_regex, view.substr(region))
    if match and len(match.groups()) < 1:
        msg = "check your snippet_regex '%s':" + \
              " match should have filetype value in last group but doesn't"
        sublime.error_message(msg % snippet_regex)
        return None
    # the last group should have the filetype value
    return match.groups()[-1] if match else None


def filetype_to_path(filetype):
    """
    Convert a filetype like 'python' to a package path like
    'Packages/Python/Python.tmLanguage", by checking first the
    'user_filetype_package_map' setting, and if not found there,
    returning the mapping in 'default_filetype_package_map' if
    there is one, and falling back to returning the 'filetype' itself,
    which allows the user to specify a full package path inline in the
    file if they don't want to define a custom mapping in the settings file.
    """
    user_map = get_setting('user_filetype_package_map') or {}
    default_map = get_setting('default_filetype_package_map') or {}
    package = user_map.get(filetype, default_map.get(filetype, None))
    return package or filetype


def update_filetype(view, filetype):
    new_filetype_path = filetype_to_path(filetype)
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

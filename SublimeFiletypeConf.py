import re

from sublime_plugin import TextCommand, EventListener

## TODO: add settings to control whether we check on post_save as well as
# on load, and perhaps allow a user-configurable filetype map and some
# other niceties

SETTINGS_REGEX = r'(?:sublimeconf):\s+filetype=([\w][\w\./ ]+)'

DEFAULT_FILETYPE_MAP = {
    'python': 'Packages/Python/Python.tmLanguage',
    'shell': 'Packages/ShellScript/Shell-Unix-Generic.tmLanguage',
    'markdown': 'Packages/Markdown/Markdown.tmLanguage'
}


def find_filetype(view):
    # find the region for the first filetype conf snippet
    region = view.find(SETTINGS_REGEX, 0)
    # if there is one, extract the filetype value from the snippet
    match = re.match(SETTINGS_REGEX, view.substr(region))
    return match.group(1) if match else None


def update_filetype(view, filetype):
    try:
        new_filetype_path = DEFAULT_FILETYPE_MAP[filetype.lower()]
    except AttributeError:
        # use it as is, on the assumption that the user gave a complete path
        # like 'Packages/Python/Python.tmLanguage' instead of just 'python'
        new_filetype_path = filetype

    # only set the syntax if it would change it from the current syntax
    curr_filetype_path = view.settings().get('syntax')
    if new_filetype_path != curr_filetype_path:
        view.set_syntax_file(new_filetype_path)


def process_view_filetype(view):
    filetype = find_filetype(view)
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
        process_view_filetype(view)


# sublimeconf: filetype=python

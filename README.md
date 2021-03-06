SublimeFiletypeConf
===================

[//]: # (sublimeconf: filetype=markdown)

Overview
========

```SublimeFiletypeConf``` is a very simple SublimeText3 plugin that sets the
syntax for a file if it finds a certain configuration snippet inside the
file. My primary use case was for files that don't have an extension in the
filename, which SublimeText will leave as plain-text files, forcing you to
manually set the syntax every time you open that file.

An example is worth a thousand words, so here is what you would include in
some file to ensure SublimeText knows that it's a Python file:

```
# sublimeconf: filetype=python
```

The snippet may appear anywhere in the file, and only the first such snippet
found is processed.

The [Modelines](https://github.com/SublimeText/Modelines) plugin provides
this sort of functionality, and much else too, but I wanted a simpler syntax
that allows me to specify the filetype as just ```python``` rather than the
verbose ```Packages/Python/Python.tmLanguage```. Plus, it gives me an excuse to
play with the SublimeText API for the first time.


Status
======

This plugin is primarily for my own personal use, but it's public in case
it's of use to anybody else. If anybody else actually ends up using it,
then I might look into polishing it up and getting it into
[Package Control](https://sublime.wbond.net/). Let me know if you'd be
interested in using it.

To try out the plugin, clone this repository and create a
symlink for the repo into the ```Packages``` directory. On Linux, this means
that after I cloned the repo as (for example) ```~/SublimeFiletypeConf```,
I then symlinked that repo directory to

```
~/.config/sublime-text-3/Packages/SublimeFiletypeConf
```

Key Binding and Command
=======================

The default key binding to check a file for a filetype snippet and apply it is
```ctrl+shift+d``` on Linux and Windows, and `super+shift+d` on OS X, but it
can easily be changed in the user keybinding settings.

There is also a command available that does the same check-and-apply process.
If you open the ```Command Palette```, typing ```Detect``` should narrow
down the options to the command, which is titled
```SublimeFiletypeConf: Detect Filetype```.


Settings
========

All the builtin SublimeText syntax types should be supported. See the
```default_filetype_package_map``` in the
```filetypeconf.sublime-settings``` file for those mappings.

The custom settings described below may be added to the user settings
file for this plugin, which will be located in ```Packages/User```. On
my Linux setup, this file is located at:

```
~/.config/sublime-text-3/Packages/User/filetypeconf.sublime-settings
```

user_filetype_package_map
-------------------------

You can define additional mappings in a user settings file by supplying
a ```user_filetype_package_map``` property. For example, if you have
defined a syntax file with a package path of
```Packages/myfiletype/myfiletype.tmLanguage```, then you could define a
mapping for that syntax by setting your user settings file to:

``` json
{
    "user_filetype_package_map": {
        "myfiletype": "Packages/myfiletype/myfiletype.tmLanguage"
    }
}
```

And then you would specify this syntax for a file by including
```sublimeconf: filetype=myfiletype``` somewhere inside a file.


on_post_save
------------

The default behavior is that a file is only parsed on load
to detect the filetype mapping, so adding a mapping to a file and then saving
the file won't change the syntax. You'd have to either close and open the file
or use the 'Reopen with Encoding' feature of SublimeText.

If you'd prefer to have every file checked after every save, in order to avoid
needing to reopen the file, you can add the following setting to the user
settings file:

``` json
{
    "on_post_save": true
}
```

snippet_regex
-------------

If you wish to use a custom regular expression to match a text snippet that
contains the filetype configuration, you can define one using the
```snippet_regex``` setting in your user settings file.

The regex string you supply must escape any backslashes in the JSON, and
your regex should match the filetype value (the ```myfiletype``` in the
example above) in the last group.

For example, if you wanted to match a simplified Vim-modeline-like syntax
that only allows ```vim:``` plus some whitespace and then a
```set filetype=VALUE`` part, you could set the following in your user
settings file:

``` json
{
    "snippet_regex": "vim:\\s+set\\s+filetype=(\\w+)"
}
```

See the built-in ```snippet_regex``` in the default plugin settings file
for an example of a more complete regex that allows for more characters
than the ```\\w+``` given above.

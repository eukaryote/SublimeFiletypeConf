SublimeFiletypeConf
===================

[//]: # (sublimeconf: filetype=markdown)

Introduction
------------

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
that allows me to specify the filetype as just 'python' rather than the
verbose 'Packages/Python/Python.tmLanguage'. Plus, it gives me an excuse to
play with the SublimeText API for the first time.

Status
------

This plugin isn't yet stable, and is primarily for my own personal use, but
it's public in case it's of use to anybody else. If anybody else actually
ends up using this, then I might look into polishing things
it up and getting it into [Package Control](https://sublime.wbond.net/) once
things stabilize a bit more. Let me know if you'd be interested.


Settings
--------

All the builtin SublimeText syntax types should be supported. See the
```default_filetype_package_map``` in the
```SublimeFiletypeConf.sublime-settings``` file for those mappings.

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

To try out this plugin, clone this repository and create a
symlink for the repo into the ```Packages``` directory. On Linux, this means
that after I cloned the repo as (for example) ```~/SublimeFiletypeConf```,
I then symlinked that repo directory to

```
~/.config/sublime-text-3/Packages/SublimeFiletypeConf
```

Additionally, the default behavior is that a file is only parsed on load
to detect the filetype mapping, so adding a mapping to a file and then saving
the file won't change the syntax. You'd have to either close and open the file
or use the 'reopen with encoding' feature of SublimeText.

If you'd prefer to have every file checked after every save, in order to avoid
needing to reopen the file, you can add the following setting to the user
settings file:

``` json
{
    "on_post_save": true
}
```

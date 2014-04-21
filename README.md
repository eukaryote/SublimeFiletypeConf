SublimeFiletypeConf
===================

[//]: # (sublimeconf: filetype=markdown)

Introduction
------------

SubimeFiletypeConf is a very simple SublimeText3 plugin that sets the syntax
for a file if it finds a certain configuration snippet inside the file. My
primary use case was for files that don't have an extension in the filename,
which SublimeText will leave as plain-text files, forcing you to manually
set the syntax every time you open that file.

An example is worth a thousand words, so here is what you would include in
some file to ensure SublimeText knows that it's a Python file:

```
# sublimeconf: filetype=python
```

The snippet may appear anywhere in the file, and only the first snippet
found is processed.

The [Modelines](https://github.com/SublimeText/Modelines) plugin provides
this sort of functionality, and much else too, but I wanted a simpler syntax
that allows me to specify the filetype as just 'python' rather than the
verbose 'Packages/Python/Python.tmLanguage'. Plus, it gives me an excuse to
play with the SublimeText API for the first time.

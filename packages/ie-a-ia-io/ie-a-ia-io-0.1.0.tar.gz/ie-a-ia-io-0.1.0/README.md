# Incredibly Easy and Instantly Accessible Input Output

Class `IOUtils` with intuitive function names for basic petty I/O streams.

Many times there's no need to have fine-grained control over some I/O. Hence the idea to pack boilerplate code (e.g. the one in `os`,`glob`) in functions with intuitive names.

## glob.os

The first aim is to pack in single functions otherwise long code snippets for operations done via the `os` or `glob` module. For instance, instead of having in the script something like this:

```
if not glob.os.path.exists(path):
    glob.os.makedirs(path)
```

Simply write `IOUtils.mkdir(path)`. This also allows to have basic `glob` and `os` functions in a single place. For instance, get all the files in a folder recursively by extension with : `IOUtils.ioglob(path,ext='txt',recursive=True)`.

## JSON and pickle

It is often the case that for several reasons one need to (1) create simple configuration files or (2) load samll python object (e.g. dictionaries) across scripts. For this use case there's no need to have the fine-grained control provided by `json` and `pickle` modules. Hence `IOUtils` has `load_json`/`save_json` and `load_pickle`/`save_pickle` for these cases.











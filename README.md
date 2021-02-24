# hf

an EXPERIMENTAL PHOTO MANAGER

## UNIMPLEMENTED Features

Cache files are under `hf_dir`

```bash
# set
$ hf config hf_dir "~/Dropbox/hf/"

# check
$ hf config hf_dir
~/Dropbox/hf/
```

Add a photo/image.

```bash
$ hf add <OBJECT> [ --tag <TAG> ] [ --tag <TAG> ] [OPTIONS]

OBJECT
    URL (http://, https://)
        Record the URL.
        Use --download, -d to save the file (under hf_dir).

    File path
        Record the full abs path.
        Use --copy, -c to copy the file (under hf_dir).
```

This is an alias for `hf add ...`.

```bash
$ hf a ...
```

Delete photo.

```bash
$ hf del <OBJECT>

OBJECT
    URL
        ...
    File path
        ...
    Object ID
        This can viewed with `hf inspect` or from the output of `hf add`
```

List up photos/images.

```bash
$ hf tail [ -n <N> ]
```

shows the last `N` records.

Grep by tags

```
$ hf grep <TAG>
$ hf grep -o <TAG> <TAG> ...  # OR-search
$ hf grep -a <TAG> <TAG> ...  # AND-search
```

List up tags.

```bash
$ hf tags
```

Add tags on a photo/image.

```bash
$ hf tags add <OBJECT> <TAG> [<TAG>...]
```

Delete tags from a photo/image.

```bash
$ hf tags del <OBJECT> <TAG> [<TAG>...]
```

Inspect a photo/image.

```bash
$ hf show <OBJECT>
```

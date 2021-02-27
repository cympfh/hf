# hf

An EXPERIMENTAL Tag-based Photos/Images Manager

## Configure

```bash
export HF_DIR=/path/to/hf/cache/dir
```

## Requirements

- sqlite3
- For twitter URL
    - twurl
    - jq

## Commands

Add a photo/image.

```
$ hf add <OBJECT> [ --tag <TAG> ] [ --tag <TAG> ] [OPTIONS]

OBJECT
    URL (http://, https://) for Photos/Images
        Record the URL.
        Use --download, -d to save the file

    URL for tweets
        including photos
        Use --download, -d to save the files
        Required: `twurl`

    File path
        Record the full abs path.
        Use --copy, -c to copy the file
```

This is an alias for `hf add ...`.

```
$ hf a ...
```

Delete photo.

```
$ hf del <OBJECT>

OBJECT
    URL
        ...
    File path
        ...
    Object ID
        This can viewed with `hf show` or from the output of `hf add`
```

List up photos/images.

```
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

```
$ hf tags
```

Add tags on a photo/image.

```
$ hf tags add <OBJECT> <TAG> [<TAG>...]
```

Delete tags from a photo/image.

```
$ hf tags del <OBJECT> <TAG> [<TAG>...]
```

Inspect a photo/image.

```
$ hf show <OBJECT>
```

## TODO

- TODO add
    - [x] Check duplication [2021/02/27 (Sat) 00:23]
    - [x] Files [2021/02/26 (Fri) 23:38]
    - [x] Image Url [2021/02/27 (Sat) 00:20]
    - [x] Tweet Url [2021/02/28 (Sun) 01:44]
    - ...
- DONE del [2021/02/27 (Sat) 01:22]
- TODO grep
    - [x] Single Tag [2021/02/26 (Fri) 23:42]
    - [ ] AND grep
    - [ ] OR grep
- TODO tags
    - [x] List up [2021/02/28 (Sun) 01:44]
    - [ ] add
    - [ ] del
- DONE tail
- DONE show [2021/02/27 (Sat) 01:22]

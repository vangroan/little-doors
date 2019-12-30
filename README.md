
# little doors

## Developing

Ensure Git Large file Storage is installed before cloning. If the repo is cloned
before install git lfs, resource files can be retrieved after the fact using:

```sh
$ git lfs fetch
$ get lfs checkout
```

Building art assets requires [Aseprite](https://www.aseprite.org/). Ensure the
`aseprite` executable is either in the `PATH` environment variable, or in otherwise
accessible from a shell.

More details at [Aseprite - Docs - Cli](https://www.aseprite.org/docs/cli/#platform-specific-details)

## Build Assets

Export Aseprite animations.

```sh
$ aseprite-b art/filename.aseprite --save-as art/filename-{tag}-1.png 
```

Copy assets to resources directory.

```sh
$ python manage.py assets
```

# Nanome - Structure Prep

A plugin to add bonds and secondary structures to complexes. Useful for Nanome Quest, as those features are not available natively.

### Preparation

Install the latest version of [Python 3](https://www.python.org/downloads/)

| NOTE for Windows: replace `python3` in the following commands with `python` |
| - |

Install the latest `nanome` lib:

```sh
$ python3 -m pip install nanome --upgrade
```

### Installation

To install Structure Prep:

```sh
$ python3 -m pip install nanome-structure-prep
```

### Usage

To start Structure Prep:

```sh
$ nanome-structure-prep -a <plugin_server_address>
```

### Docker Usage

To run Structure Prep in a Docker container:

```sh
$ cd docker
$ ./build.sh
$ ./deploy.sh -a <plugin_server_address>
```

### Development

To run Structure Prep with autoreload:

```sh
$ python3 run.py -a <plugin_server_address>
```

### License

MIT

# pytna
[![PyPI version](https://badge.fury.io/py/etna-cli.svg)](https://badge.fury.io/py/etna-cli)
[![Build Status](http://drone.matteyeux.com:8080/api/badges/matteyeux/etna-cli/status.svg)](http://drone.matteyeux.com:8080/matteyeux/etna-cli)
[![Packagist](https://img.shields.io/badge/Docs-etna-blue)](http://collab-mha.nexen.net/etna-cli) 

Python tool for my school

### Usage

```
Usage: etna.py [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  print version
  --help         Show this message and exit.

Commands:
  config        Init, edit or delete etna config.
  conversation  Conversations on intranet.
  declare       Declaration.
  event         Events.
  gitlab        Gitlab.
  project       Projects.
  rank          Rank by promotion.
  student       Student stuff.
  task          Add quests and projects to TaskWarrior.
  ticket        Tickets.
```


### Installation

Make sure to have `taskwarrior` installed to task related stuff

#### Github repository
```bash
$ git clone https://github.com/matteyeux/etna-cli
$ cd etna-cli
$ poetry install
```

#### PyPI
- Installation : `pip3 install etna-cli`
- Update : `pip3 install --upgrade etna-cli`

### Setup

If you run etna-cli for the first time you may run `etna config init` to set credentials and optional Gitlab Token.
```
$ etna config init
ETNA username : demo_t
Password:
Add Gitlab API token ? [Y/n]: Y
Gitlab API token :
```

Password and Gitlab token are not printed to STDOUT.


### Credits
Powered by [etnawrapper](https://github.com/tbobm/etnawrapper)



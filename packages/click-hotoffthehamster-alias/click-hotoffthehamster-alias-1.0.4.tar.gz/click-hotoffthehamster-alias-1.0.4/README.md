# click-hotoffthehamster-alias

[![build](https://travis-ci.com/hotoffthehamster/click-hotoffthehamster-alias.svg?branch=release)](https://travis-ci.com/hotoffthehamster/click-hotoffthehamster-alias)
[![license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://raw.githubusercontent.com/hotoffthehamster/click-hotoffthehamster-alias/release/LICENSE)
[![coverage](https://coveralls.io/repos/github/hotoffthehamster/click-hotoffthehamster-alias/badge.svg?branch=release)](https://coveralls.io/github/hotoffthehamster/click-hotoffthehamster-alias?branch=release)

Add (multiple) aliases to a click_ group or command.

In your [click](http://click.pocoo.org/) app:

```python
import click_hotoffthehamster as click
from click_hotoffthehamster import ClickAliasedGroup

@click.group(cls=ClickAliasedGroup)
def cli():
    pass

@cli.command(aliases=['bar', 'baz', 'qux'])
def foo():
    """Run a command."""
    click.echo('foo')
```

Will result in:
```
Usage: cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  foo (bar,baz,qux)  Run a command.
```

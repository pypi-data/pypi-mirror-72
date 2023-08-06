import click_hotoffthehamster as click
from click_hotoffthehamster.testing import CliRunner

from click_hotoffthehamster_alias import ClickAliasedGroup

import pytest


@pytest.fixture(scope="function")
def runner():
    return CliRunner()


@click.group(cls=ClickAliasedGroup)
def cli():
    pass


@cli.command(aliases=['bar'])
def foo():
    click.echo('foo')


TEST_HELP = """Usage: cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  foo (bar)
"""


def test_help(runner):
    result = runner.invoke(cli)
    assert result.output == TEST_HELP


def test_foobar(runner):
    for cmd in ['foo', 'bar']:
        result = runner.invoke(cli, [cmd])
        assert result.output == 'foo\n'


TEST_INVALID = """Usage: cli [OPTIONS] COMMAND [ARGS]...
{}
Error: No such command 'baz'.
""".format("Try 'cli --help' for help.\n")


def test_invalid(runner):
    result = runner.invoke(cli, ['baz'])
    assert result.output == TEST_INVALID

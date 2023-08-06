"""
    Extension for the python ``click`` module
    to provide a group or command with aliases.
"""

import click_hotoffthehamster as click


class ClickAliasedGroup(click.Group):
    def __init__(self, *args, **kwargs):
        super(ClickAliasedGroup, self).__init__(*args, **kwargs)
        self._commands = {}
        self._aliases = {}

    def command(self, *args, **kwargs):
        aliases = kwargs.pop('aliases', [])
        decorator = super(ClickAliasedGroup, self).command(*args, **kwargs)
        if not aliases:
            return decorator

        def _decorator(f):
            cmd = decorator(f)
            if aliases:
                self._commands[cmd.name] = aliases
                for alias in aliases:
                    self._aliases[alias] = cmd.name
            return cmd

        return _decorator

    def group(self, *args, **kwargs):
        aliases = kwargs.pop('aliases', [])
        decorator = super(ClickAliasedGroup, self).group(*args, **kwargs)
        if not aliases:
            return decorator

        def _decorator(f):
            cmd = decorator(f)
            if aliases:
                self._commands[cmd.name] = aliases
                for alias in aliases:
                    self._aliases[alias] = cmd.name
            return cmd

        return _decorator

    def resolve_alias(self, cmd_name):
        if cmd_name in self._aliases:
            return self._aliases[cmd_name]
        return cmd_name

    def get_command(self, ctx, cmd_name):
        cmd_name = self.resolve_alias(cmd_name)
        command = super(ClickAliasedGroup, self).get_command(ctx, cmd_name)
        if command:
            return command

    # (lb): I forked Click and split up Click's base function,
    # MultiCommand.format_commands, into pieces, so that we can
    # just add the lines of new code we need and do nothing else.
    # (But that's not the only reason I forked Click!)
    def format_commands_fetch(self, ctx):
        commands = []
        _commands = super(ClickAliasedGroup, self).format_commands_fetch(ctx)
        for subcommand, cmd in _commands:
            if subcommand in self._commands:
                aliases = ','.join(sorted(self._commands[subcommand]))
                subcommand = '{0} ({1})'.format(subcommand, aliases)
            commands.append((subcommand, cmd))
        return commands

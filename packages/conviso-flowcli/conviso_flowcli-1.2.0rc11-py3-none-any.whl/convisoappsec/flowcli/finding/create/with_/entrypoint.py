import click

from convisoappsec.flowcli import help_option

from .version_tracker import version_tracker


@click.group('with')
@help_option
def with_():
    pass

with_.add_command(version_tracker)
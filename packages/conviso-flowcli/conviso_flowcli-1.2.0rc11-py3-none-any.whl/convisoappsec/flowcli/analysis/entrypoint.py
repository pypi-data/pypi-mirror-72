import click

from convisoappsec.flowcli import help_option
from .sast import sast

@click.group()
@help_option
def analysis():
    pass


analysis.add_command(sast)

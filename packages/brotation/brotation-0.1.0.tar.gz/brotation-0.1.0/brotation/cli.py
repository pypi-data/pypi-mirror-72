"""Console script for brotation."""
import wingdbstub
import sys
import click

from .brotation import BackupRotator


@click.group()
def grun():
    pass


@grun.command()
@click.option('-w', '--where', 'where')
@click.option('-f', '--folders', 'folders')
@click.option('-f', '--config', 'config')
def backup(where, folders, config):
    """*Create rotated compressed backups.*
    
    --where: root of destination rotated backups.
    --folders: which folders must be compressed.
    --config: path to backups.conf to automatically extract which folders must be compressed.
    
    Note:
    
    --config values are used as default values over --where or --folders.
    
    """
    # click.echo(where)
    # click.echo(folders)
    rot = BackupRotator(where, folders, config)

    today = rot.today()
    changes = rot.rotations(today)
    rot.apply(changes)

    foo = 1


@grun.command()
@click.option('-w', '--where', 'where')
@click.option('-n', '--name', 'name')
@click.option('-a', '--age', 'age')
@click.option('-d', '--date', 'date')
def restore(where, folders, name):
    """Command on g1"""
    click.echo(where)
    click.echo(name)
    click.echo(age)
    click.echo(date)
    rot = BackupRotator(where, folders)

    foo = 1


@click.group()
def gsystem():
    pass


@gsystem.command()
@click.option('-d', '--time', 'date')
def install():
    """install service
    
[Unit]
Description=Daily apt download activities

[Timer]
OnCalendar=*-*-* 6,18:00
RandomizedDelaySec=12h
Persistent=true

[Install]
WantedBy=timers.target


[Unit]
Description=Daily rotation of log files
Documentation=man:logrotate(8) man:logrotate.conf(5)

[Timer]
OnCalendar=daily
AccuracySec=12h
Persistent=true

[Install]
WantedBy=timers.target

[Unit]
Description=Message of the Day

[Timer]
OnCalendar=00,12:00:00
RandomizedDelaySec=12h
Persistent=true
OnStartupSec=1min

[Install]
WantedBy=timers.target

    
    """


@gsystem.command()
def uninstall():
    """install service"""


@gsystem.command()
def pause():
    """install service"""


main = click.CommandCollection(sources=[g1, g2])

if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover

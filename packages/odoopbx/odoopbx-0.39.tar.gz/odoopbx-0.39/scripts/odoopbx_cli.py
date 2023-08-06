import click
import json
import logging
import os
import sys
import shutil
import subprocess
import yaml
import odoopbx
import odoopbx.scripts

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

SALT_PATH = '/etc/odoopbx'


def _update_salt_files():
    # Copy salt files and folders from package directory.
    click.echo('Updating salt files...')
    mydir = os.path.dirname(os.path.abspath(__file__))
    salt_dir = os.path.join(mydir, '..', 'salt')
    # Copy folders
    for f in [
            'extensions',
            'minion.d',
            'pillar',
            'roots',
            ]:
        target = os.path.join(SALT_PATH, f)
        # Remove old version
        if os.path.exists(target):
            shutil.rmtree(target)
        shutil.copytree(os.path.join(salt_dir, f), target)
    # Copy/overwrite files
    for f in ['minion', 'Saltfile']:
        open(os.path.join(SALT_PATH, f), 'w').write(
            open(os.path.join(salt_dir, f)).read())
    # Put a .salted file so that we do not copy on every start.    
    open(os.path.join(SALT_PATH, '.salted'), 'w').write(
        odoopbx.scripts.__version__)


@click.group()
def main():
    # Check for /etc/odoopbx folder
    if not os.path.exists(SALT_PATH):
        os.mkdir(SALT_PATH)
        _update_salt_files()
    # Check for flag to update salt files
    salted_file = os.path.join(SALT_PATH, '.salted')
    if not os.path.exists(salted_file):
        _update_salt_files()
    elif open(salted_file).read() != odoopbx.scripts.__version__:
        _update_salt_files()
    if not os.path.exists(os.path.join(SALT_PATH, 'local.conf')):
        # Copy default files
        conf_files_path = os.path.join(SALT_PATH, 'minion.d')
        custom_conf = open('/etc/odoopbx/local.conf', 'w')
        for f in [k for k in os.listdir(conf_files_path) if k.endswith(
                '.conf') and not k.startswith('_')]:
            custom_conf.write(
                open(os.path.join(
                    SALT_PATH, 'minion.d', f)).read())
        custom_conf.close()
    # Change working folder to Odoo PBX Salt package.
    os.chdir(SALT_PATH)


@main.command(help='Call a command.')
@click.argument('cmd', nargs=-1)
def call(cmd):
    """
    Execute a salt-call command passing all parameters.
    To pass an option use -- e.g. odoopbx call -- --version
    """
    cmd_l = ['salt-call']
    cmd_l.extend(list(cmd))
    os.execvp('salt-call', cmd_l)


@main.group(help='Configuration management.')
def config():
    pass


def _config_load():
    config_path = os.path.join(SALT_PATH, 'local.conf')
    config = yaml.load(open(config_path), yaml.SafeLoader)
    return config


def _config_save(config):
    config_path = os.path.join(SALT_PATH, 'local.conf')
    open(config_path, 'w').write(
        yaml.dump(config, default_flow_style=False, indent=2))


@config.command(name='get')
@click.argument('option')
@click.option('--raw', is_flag=True,
              help='Fetch the value directly from .conf file instead '
                   'of internal storage.')
def config_get(option, raw):
    """
    Get a configuration option's value.
    """
    if not raw:
        os.execvp('odoopbx', ['odoopbx', 'call', 'config.get', option])
    else:
        config = _config_load()
        if option not in config:
            click.secho('Option {} not found', fg='red')
        else:
            click.echo('Value of type: {}.\n\n{}'.format(
                type(config[option]).__name__,
                yaml.dump(config[option], default_flow_style=False, indent=2)))


@config.command(name='set')
@click.argument('option')
@click.argument('value')
def config_set(option, value):
    """
    Set a configuration option passed as JSON.

    Examples:

        odoopbx config set ami_trace_actions true # true and not True
        odoopbx config set ami_trace_events '["Cdr","FullyBooted"]'

    You can verify how option value is treated by calling:

        odoopbx config get --raw ami_trace_events
    """
    try:
        value = json.loads(value)
    except json.decoder.JSONDecodeError:
        # String value
        pass
    config = _config_load()
    if option not in config:
        click.secho('Option {} not found, creating a new one.'.format(
                    option), fg='red')
    config[option] = value
    _config_save(config)


@main.group(help='Run service.',
            invoke_without_command=True)
@click.argument('service', nargs=-1, required=True)
def run(service):
    service = list(service)
    if 'agent' in service:
        service.remove('agent')
        service.insert(0, 'salt-minion')
        service.extend(['-l', 'info'])
        os.execvp('salt-minion', service)
    else:
        click.echo('Not yet implemented')


@main.command(help='Enable a service.')
@click.argument('service', required=True)
def enable(service):
    os.execvp('salt-call', ['salt-call', 'state.apply', service])


@main.command(help='Install a service / all services')
@click.argument('service')
def install(service):
    if service == 'all':
        os.execvp('salt-call', ['salt-call', '-l', 'info', 'state.highstate'])
    else:
        os.execvp('salt-call', ['salt-call', '-l', 'info', 'state.apply', service])


@main.command(help='Restart a service')
@click.argument('service')
def restart(service):
    if service == 'agent':
        service = 'odoopbx-agent'
    os.execvp('systemctl', ['systemctl', 'restart', service])


@main.group(help='Show information.')
def show():
    pass


@main.command(help='Start a service.')
@click.argument('service')
def start(service):
    # Little magic to save time.
    if service == 'agent':
        service = 'odoopbx-agent'
    os.execvp('systemctl', ['systemctl', 'start', service])


@main.command(help='Stop a service.')
@click.argument('service')
def stop(service):
    # Little magic to save time.
    if service == 'agent':
        service = 'odoopbx-agent'
    os.execvp('systemctl', ['systemctl', 'stop', service])


@show.command(help='Show system information.', name='version')
def show_version():
    click.echo('Odoo PBX CLI version {}.'.format(odoopbx.scripts.__version__))

if __name__ == '__main__':
    main()

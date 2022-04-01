# Copyright 2022 H2O.ai, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import re
import shutil
import subprocess
import sys
from pathlib import Path
import click

module_dir = Path(__file__).parent
templates_dir = module_dir / 'templates'
samples_dir = templates_dir / 'samples'
frameworks_dir = templates_dir / 'frameworks'


@click.group()
def main():
    pass


@main.command()
@click.argument('name')
@click.option(
    '--template',
    default='basic',
    help='The app template to use. Run "nitro list templates" to list available templates',
)
@click.option(
    '--framework',
    default='flask',
    help='The web framework to use. Run "nitro list frameworks" to list available frameworks.',
)
def create(name: str, template: str, framework: str):
    """Initialize a new app.

    \b
    Initialize a basic Flask app named "my_app":
    $ nitro create my_app

    \b
    Initialize a Flask app named "my_app" based on the recruitment starter app:
    $ nitro create my_app --template recruitment

    \b
    Initialize a basic Tornado app named "my_app":
    $ nitro create my_app --framework tornado

    \b
    Initialize a Starlette app named "my_app" based on the recruitment starter app::
    $ nitro create my_app --template recruitment --framework starlette

    """
    sample_dir = samples_dir / template
    if not sample_dir.is_dir():
        click.echo(f'Unknown template: {template}', err=True)
        return

    framework_dir = frameworks_dir / framework
    if not framework_dir.is_dir():
        click.echo(f'Unknown framework: {framework}', err=True)
        return

    app_dir = Path(name)
    shutil.copytree(framework_dir, app_dir)

    async_sample = (sample_dir / 'app.py').read_text()
    sync_sample = re.sub('(async |await |AsyncView as)', '', async_sample)

    app_file = app_dir / 'app.py'
    app_code = app_file.read_text()
    app_code = app_code.replace('# SAMPLE_ASYNC', async_sample)
    app_code = app_code.replace('# SAMPLE_SYNC', sync_sample)
    app_file.write_text(app_code)

    readme_file = app_dir / 'README.md'
    readme = readme_file.read_text().replace('APP_DIR', name)
    readme_file.write_text(readme)
    click.echo(readme)


def _to_numbered_list(items):
    return '\n'.join([f'{i + 1}. {x}' for i, x in enumerate(items)])


def _list_dir_names(p: Path):
    return _to_numbered_list(sorted([d.name for d in p.iterdir()]))


@main.command()
@click.argument('kind')
def list(kind: str):
    """List available templates and frameworks.

    \b
    List all available templates
    $ nitro list templates

    \b
    List all available frameworks
    $ nitro list frameworks

    """
    if kind == 'templates':
        click.echo('Available templates:')
        click.echo(_list_dir_names(samples_dir))
        return
    if kind == 'frameworks':
        click.echo('Available frameworks:')
        click.echo(_list_dir_names(frameworks_dir))
        return


@main.command()
def docs():
    """Launch Nitro's interactive documentation.
    """
    tour_file_path = str(module_dir / 'docs' / 'docs.py')
    proc = subprocess.Popen([sys.executable, tour_file_path], stdout=subprocess.PIPE)
    for line in io.TextIOWrapper(proc.stdout, encoding='utf-8'):
        print(line)


if __name__ == '__main__':
    main()

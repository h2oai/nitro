# Copyright 2020 H2O.ai, Inc.
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

import shutil
from pathlib import Path
import click


@click.group()
def main():
    pass


@main.command()
@click.argument('name')
@click.option('--template', default='basic', help='The app template to use.')
@click.option('--framework', default='flask', help='The web framework to use. One of "flask", "tornado", "starlette".')
def init(name: str, template: str, framework: str):
    """Initialize a new app.
    """
    templates_dir = Path(__file__).parent / 'templates'
    samples_dir = templates_dir / 'samples' / template
    if not samples_dir.is_dir():
        click.echo(f'Unknown template: {template}', err=True)
        return

    framework_dir = templates_dir / 'frameworks' / framework
    if not framework_dir.is_dir():
        click.echo(f'Unknown framework: {framework}', err=True)
        return

    app_dir = Path(name)
    shutil.copytree(framework_dir, app_dir)

    sync_sample = (samples_dir / 'sync.py').read_text()
    async_sample = (samples_dir / 'async.py').read_text()

    app_file = app_dir / 'app.py'
    app_code = app_file.read_text()
    app_code.replace('# SAMPLE_SYNC', sync_sample)
    app_code.replace('# SAMPLE_ASYNC', async_sample)
    app_file.write_text(app_code)

    readme_file = app_dir / 'README.md'
    readme = readme_file.read_text().replace('APP_DIR', name)
    readme_file.write_text(readme)
    click.echo(readme)


if __name__ == '__main__':
    main()

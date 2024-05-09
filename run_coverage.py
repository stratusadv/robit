import os
import subprocess
import sys

# Do not ever rename this file to coverage.py as it creates an infinite loop.
# This script must run from the root of your project.

if sys.platform != 'win32':
    raise Exception('Only the Windows platform is supported for this script.')

virtual_env = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'activate')
virtual_env_alternate = os.path.join(os.path.dirname(__file__), '.venv', 'Scripts', 'activate')

if os.path.isfile(virtual_env):
    activate_virtualenv_cmd = virtual_env
elif os.path.isfile(virtual_env_alternate):
    activate_virtualenv_cmd = virtual_env_alternate
else:
    raise Exception(f'Virtual environment "{virtual_env}" or "{virtual_env_alternate}" not found.')

pip_install_coverage_cmd = 'pip install coverage'


print('Running coverage with tests ...\n')

omits = (
    '*/system/*',
    '*/tests/*',
    '*/migrations/*',
    '*/static/*',
    '*/.venv/*',
    'apps.py',
    '__init__.py',
    'manage.py',
    'automation.py',
    'run_coverage.py',
    'setup.py',
)

coverage_run_cmd = f'coverage run --branch --source=. --omit={",".join(omits)} -m unittest discover tests'

html_directory = '.coverage_html_report'
coverage_html_cmd = f'coverage html --directory={html_directory}'

coverage_erase_cmd = f'coverage erase'

open_browser_cmd = f'start "" "{os.path.dirname(__file__)}/{html_directory}/index.html"'

cmd_call = (
    f'call {activate_virtualenv_cmd}'
    f' & {pip_install_coverage_cmd}'
    f' & {coverage_run_cmd}'
    f' & {coverage_html_cmd}'
    f' & {coverage_erase_cmd}'
    f' & {open_browser_cmd}'
)

subprocess.run(cmd_call, shell=True)

print('\nDone!')

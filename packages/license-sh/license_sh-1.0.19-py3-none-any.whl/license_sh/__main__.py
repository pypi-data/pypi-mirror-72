#!/usr/bin/env python
"""License.sh

Usage:
  license-sh config
  license-sh [options]
  license-sh <path> [options]
  license-sh (-h | --help)
  license-sh --version

Options:
  -h --help                           Show this screen.
  -o <reporter> --output <reporter>   Output [default: console].
  -t --tree                           Show full dependency tree.
  -d --debug                          Debug mode
  -p --project <project_type>         Run only specific project [yarn | npm | maven | pipenv]
  --dependencies                      Include dependency license text analysis. Suported: npm, yarn, maven
  -c --config <config_path>           Use custom path to config       
  --version                           Show version.
"""
from docopt import docopt
from .version import __version__

from .commands.run_license_sh import run_license_sh

arguments = docopt(__doc__, version=__version__)
run_license_sh(arguments)

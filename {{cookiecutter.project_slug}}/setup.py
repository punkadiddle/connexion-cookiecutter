#!/usr/bin/env python3
import os
import re
import subprocess
from setuptools import setup


args = {}

if os.path.isdir('.git'):
    result = subprocess.run(['git', 'describe', '--tags', '--match', 'v*', '--dirty'], stdout=subprocess.PIPE)
    if result.returncode == 0:
        version = result.stdout.decode("utf-8").splitlines()[0]
        args['version'] = re.sub(r'-g([0-9a-f]+)', r'+git\1', version)
        open('.version', 'w', encoding='utf-8').write(args['version'])

elif os.path.exists('.version'):
    args['version'] = open('.version', 'r', encoding='utf-8').read()

    # TODO: currently not working with semver versions
    #args['use_scm_version'] = {
    #    'write_to': '.version',
    #    'write_to_template': '{version}',
    #    'tag_regex': r'^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$',
    #}

else:
    args['version'] = '0.0.0'

setup(**args)

import os
import shutil


project_slug = '{{cookiecutter.project_slug}}'
use_reldb = '{{cookiecutter.use_reldb}}'
use_ui = '{{cookiecutter.use_ui}}'

src_module_path = os.path.join(os.path.abspath(os.path.curdir), 'src', project_slug)

if not use_reldb.startswith('y'):
    shutil.rmtree(os.path.join(src_module_path, 'model'))

if not use_ui.startswith('y'):
    shutil.rmtree(os.path.join(src_module_path, 'ui'))

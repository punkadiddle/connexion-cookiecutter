import re
import sys
from textwrap import dedent

NAME_REGEX = r'^([a-z][_a-z0-9]+(?:\.|$)){2,4}'

d = {
    'project_slug': '{{ cookiecutter.project_slug }}',
}

msg = []
# if not re.match(NAME_REGEX, d['project_slug']):
#     msg.append("""\
#         Ungültiger project_slug '{project_slug}'.
#         PEP432 Python-Module Name soll aus 2-3 Segmenten [a-z][a-z0-9_] bestehen, die durch Punkte getrennt werden.")
#         Das erste Element spiegelt den Eigentümer wieder, das letzte Element ist der eigentliche Modulname.
#     """)
    
for x in msg:
    print(dedent(x).format(**d), file=sys.stderr)

if len(msg) > 0:
    # exits with status 1 to indicate failure
    sys.exit(1)

import argparse
import os
import sys

from paste.deploy import loadapp
from flask_script import Manager


def main():
    parser = argparse.ArgumentParser(description='Process some integers.', add_help=False)
    parser.add_argument('-h', '--help', dest='help', action='store_true')
    parser.add_argument('--paste', dest='config', action='store', default=None,
                        help='an integer for the accumulator')
    
    # Unbekannte Argument +Hilfe an Manager weitergeben
    args, unknownArgs = parser.parse_known_args()
    sys.argv = sys.argv[0:1]
    if args.help:
        parser.print_help()
        sys.argv.append('--help')
    sys.argv += unknownArgs
    
    if args.config:
        if not os.path.isfile(args.config):
            print('Konfiguration nicht gefunden: %s' % (args.config,), file=sys.stderr)
            return 1
        
        # WSGI App mit Konfiguration initialisieren
        app = loadapp('config:/' + args.config)
        
        # Flask Scripting konfigurieren
        manager = Manager(app)

        {% if cookiecutter.use_reldb.startswith('y') %}
        from flask_migrate import MigrateCommand
        manager.add_command('db', MigrateCommand)
        {% endif -%}
        
        return manager.run()
        
    else:
        print("--paste <CONFIG> ist erforderlich!", file=sys.stderr)
        return 1
    
if __name__ == '__main__':
    sys.exit(main())

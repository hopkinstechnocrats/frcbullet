from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from frcbullet.cli.core.exc import TodoError
from frcbullet.cli.controllers import Base

# configuration defaults
CONFIG = init_defaults('todo')
CONFIG['todo']['foo'] = 'bar'
CONFIG['todo']['db_file'] = '~/.todo/db.json'
CONFIG['todo']['email'] = 'you@yourdomain.com'


class Todo(App):
    """FRCBullet primary application."""

    class Meta:
        label = 'frcbullet'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        close_on_exit = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
        ]

        # register hooks
        hooks = [

        ]


class TodoTest(TestApp, Todo):
    """A sub-class of Todo that is better suited for testing."""

    class Meta:
        label = 'todo'


def main():
    with Todo() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except TodoError as e:
            print('TodoError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()

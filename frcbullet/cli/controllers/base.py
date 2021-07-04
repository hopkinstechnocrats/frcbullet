import asyncio

from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
import frcbullet.core

VERSION_BANNER = """
FRCBullet:  %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'FRCBullet'

        # text displayed at the bottom of --help output
        epilog = 'Usage: frcbullet'

        # controller level arguments. ex: 'todo --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()


    @ex(
        help='Run WPILib Desktop simulation in the current directory and connect to Bullet Physics Engine',

        # arguments=[
        #     ### add a sample foo option under subcommand namespace
        #     ( [ '-f', '--foo' ],
        #       { 'help' : 'notorious foo option',
        #         'action'  : 'store',
        #         'dest' : 'foo' } ),
        # ],
    )
    def simulate(self):
        """Run WPILib Desktop simulation in the current directory and connect to Bullet Physics Engine"""
        asyncio.run(frcbullet.core.run())


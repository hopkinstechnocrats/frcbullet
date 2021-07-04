
from setuptools import setup, find_packages
from frcbullet.cli.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='frcbullet',
    version=VERSION,
    description='Interface between WPILib Desktop Simulation and Bullet Physics Engine',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Henry Scheible',
    author_email='henry.scheible@gmail.com',
    url='https://github.com/hopkinstechnocrats/frcbullet',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'frcbullet': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        frcbullet = frcbullet.cli.main:main
    """,
)

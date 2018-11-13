"""``tamago`` lives on
https://github.com/hhollenstain/tamago
"""
from setuptools import setup, find_packages
import tamago

INSTALL_REQUIREMENTS = [
    'asyncio',
    'aiomeasures',
    'coloredlogs',
    'over_stats',
    'oyaml',
    'PyNaCl',
    'pyowm',
    'python-overwatch',
    'pyyaml',
    'requests==2.19.1',
    'youtube_dl'
]

TEST_REQUIREMENTS = {
    'test':[
        'pytest',
        'pylint',
        'sure',
        ]
    }

DEPENDENCY_LINKS = [
    'git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py==1.0.0',
]

setup(
    name='tamago',
    version=tamago.VERSION,
    description='Tamgo Discord Bot',
    url='https://github.com/hhollenstain/tamago',
    packages=find_packages(),
    include_package_data=True,
    install_requires=INSTALL_REQUIREMENTS,
    extras_require=TEST_REQUIREMENTS,
    entry_points={
        'console_scripts':  [
            'tamago = tamago.tamago_bot:main',
        ],
    },
    )

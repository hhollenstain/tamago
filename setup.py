"""``tamago`` lives on
https://github.com/hhollenstain/tamago
"""
from setuptools import setup, find_packages
import tamago

INSTALL_REQUIREMENTS = [
    'asyncio',
    'aiomeasures',
    'coloredlogs',
    'discord.py==1.1.1',
    'over_stats',
    'oyaml',
    'pip==18.0',
    'PyNaCl',
    'pyowm==2.9.0',
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

"""``tamago`` lives on
https://github.com/hhollenstain/tamago
"""
from setuptools import setup, find_packages
import tamago

INSTALL_REQUIREMENTS = [
    'asyncio',
    'coloredlogs',
    'discord.py',
    'flask',
    'PyNaCl',
    'waitress',
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

"""``tamago`` lives on
https://github.com/hhollenstain/tamago
"""
from setuptools import setup, find_packages
import tamago

INSTALL_REQUIREMENTS = [
    'asyncio',
    'coloredlogs',
    'discord.py',
    'PyNaCl',
    'youtube_dl'
]

SETUP_REQUIRES = [
    'discord==1.0.0'
]

DEPENDENCY_LINK = [
    'https://github.com/Rapptz/discord.py/tarball/rewrite#egg=discord-1.0.0a',
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
    #dependency_links=DEPENDENCY_LINK,
    #setup_requires=SETUP_REQUIRES,
    description='Tamgo Discord Bot',
    url='https://github.com/hhollenstain/tamago',
    packages=find_packages(),
    include_package_data=True,
    install_requires=INSTALL_REQUIREMENTS,
    extras_require=TEST_REQUIREMENTS,
    entry_points={
        'console_scripts':  [
            'tamago = tamago.tamago:main',
        ],
    },
    )

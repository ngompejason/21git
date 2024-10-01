from setuptools import setup

setup(name = '21git',
        version = '1.0',
        packages=['21git'],
        entry_points = {
            'console_scripts':[
                '21git = 21git.cli:main'
            ]
        })
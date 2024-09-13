from setuptools import setup

setup(name = 'ugit',
        version = '1.0',
        packages=['ugit'],
        entry_points = {
            'console_scripts':[
                '21git = ugit.cli:main'
            ]
        })
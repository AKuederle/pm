from setuptools import setup

setup(
    name='pm',
    version='',
    packages=['project_manager'],
    url='',
    license='',
    author='arne',
    author_email='',
    description='A simple commandline project manager',

    entry_points={
        'console_scripts': [
            'pm=project_manager.scripts.pm:main',
            '_p=project_manager.scripts.p:main'
        ],
    }
)

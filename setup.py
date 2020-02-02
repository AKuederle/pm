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
    scripts=['project_manager/scripts/p'],
    entry_points={
        'console_scripts': [
            '_p=project_manager.scripts.p:main'
        ],

    }
)

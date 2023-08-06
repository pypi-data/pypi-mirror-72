from setuptools import setup

files = ['./*']

setup(
    name='tide-query',
    version='0.0.1',
    description='This is a spider helper.',
    author='Jover Zhang',
    author_email='joverzh@gmail.com',
    packages=[''],
    package_data={'./': files},
    install_requires=[
        'requests',
        'beautifulsoup4',
    ]
)

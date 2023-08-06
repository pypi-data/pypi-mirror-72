from setuptools import setup
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
    readme = f.read()

setup(
    name='pflogf',
    version='0.0.2rc2',
    author='Jennings Zhang',
    author_email='Jennings.Zhang@childrens.harvard.edu',
    description='Logging formatter for fnndsc/pf* family, inspired by pfmisc.debug',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/FNNDSC/pflogf',
    license='MIT',
    keywords='logging color',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
    ],

    python_requires='>=3.6',
    install_requires=['colorlog~=4.1.0'],

    py_modules=['pflogf'],
    entry_points={'console_scripts': ['pflogf = pflogf:examples']},
)

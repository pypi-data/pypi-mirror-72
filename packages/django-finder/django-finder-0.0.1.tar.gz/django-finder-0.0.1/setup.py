from setuptools import setup
import os

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-finder',
    version = '0.0.1',
    description = 'A Django app to find car make/model/year from photo.',
    long_description = 'README.rst',
    url = 'https://github.com/GaboxFH/cis4930-carfinder',
    author = 'Gabriel Fernandez, Bao Nguyem, Kyle Bradley, Ziyad Morsi, Eric Gorday',
    author_email = 'kyle.bradley@ufl.edu',
    license = 'UF License',  # Example license
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',  # Replace "X.Y" as appropriate',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

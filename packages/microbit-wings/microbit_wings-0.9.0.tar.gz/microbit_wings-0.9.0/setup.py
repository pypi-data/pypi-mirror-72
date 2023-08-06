"""
Kommunikationstreiber für das Lehrmittel Computertechnik und Programmierung
der Wings Lernmedien.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    # Project name
    # $ pip install microbit_wings
    # it will live on PyPI: https://pypi.org/project/microbit_wings/
    name='microbit_wings',  # Required
    version='0.9.0',  # Required
    description='Communication driver for the Microbit',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)

    # This field corresponds to the "Home-Page" metadata field:
    url='https://github.com/',  # Optional

    # This should be your name or the name of the organization which owns the project.
    author='Pascal Helfenstein',  # Optional

    # This should be a valid email address corresponding to the author listed above.
    # author_email='pypa-dev@googlegroups.com',  # Optional

    # Classifiers help users find your project by categorizing it.
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 3.6',
    ],

    # This field adds keywords for your project.
    keywords='education learning microbit wings-lernmedien',  # Optional

    # Root of the source directory
    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'),  # Required

    # Include ini files
    package_data={'': ['*.ini']},

    # Specify which Python versions you support.
    python_requires='>=3.6',

    # This field lists other packages that your project depends on to run.
    install_requires=['pyserial'],  # Optional

    # List additional URLs that are relevant to your project as a dict.
    project_urls={'a': 'http://www.a.com/',
                  'b': 'http://www.b.com/',
                  'Source': 'https://github.com/'},  # Optional

    # project_urls={'Wings Lernmedien': 'http://www.wings.ch/',
    #               'Wings Lernmedien Lehrmittel': 'http://www.wings.ch/',
    #               'Source': 'https://github.com/todo'},  # Optional
)

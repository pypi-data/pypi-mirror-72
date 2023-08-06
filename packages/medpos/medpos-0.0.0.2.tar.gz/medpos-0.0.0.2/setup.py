from os import path
from io import open
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    INSTALL_REQUIRES = f.read().split('\n')

# # Get VERSION from the VERSION file
# with open(path.join(HERE, 'VERSION'), encoding='utf-8') as f:
#     PACKAGE_VERSION = f.read().rstrip()

PACKAGE_VERSION = '0.0.0.2'

setup(
    name='medpos',

    version=PACKAGE_VERSION,

    description='medical part-of-speech tagging',

    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    
    package_data={  # Optional
        'medpos': ['crfpp/nlptext_lite/sources/*',
                    'model/MedPos/char/T_b-n1t1-f1_m-n1t1-f1_r-n1t1-f1_P-bio_E-bio/model',
                    'model/MedPos/char/T_b-n1t1-f1_m-n1t1-f1_r-n1t1-f1_P-bio_E-bio/para.p',
                    'model/MedPos/char/T_b-n1t1-f1_m-n1t1-f1_r-n1t1-f1_P-bio_E-bio/template'],
    },

    url='',

    author='junjieluo',

    author_email='floydjjluo@gmail.com',

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='',  # Optional

    packages=find_packages(exclude=[
        'contrib',
        'docs',
        ]),  # Required

    python_requires='>=3.6, <4',

    install_requires=[] + INSTALL_REQUIRES,  # Optional

    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': [
            'coverage',
            'pytest',
            'pylint',
        ],
    },

    
)

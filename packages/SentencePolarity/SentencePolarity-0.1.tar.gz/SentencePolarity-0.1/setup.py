from setuptools import find_packages
from setuptools import setup
REQUIRED_PACKAGES = [
    'gcsfs==0.6.0',
    'google-cloud-storage==1.26.0',
    'pandas==0.24.2',
    'stemming',
    'nltk',
    'setuptools',
    'scrapy',
    'vaderSentiment',
    'scikit-learn']
PACKAGE_NAME='SentencePolarity'                        # model folder name
PACKAGE_DESCRIPTION='SentencePolarity python 3 claire'     # model folder name
setup(name=PACKAGE_NAME,
    version='1.0',
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.data", "*.csv", "*.txt", "*.tff", "*.classifier", 'lexicon'],
        # And include any *.msg files found in the "hello" package, too:
        #"hello": ["*.msg"],
    },
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description=PACKAGE_DESCRIPTION)


from distutils.core import setup
setup(
  name = 'SentencePolarity',         # How you named your package folder (MyLib)
  packages = ['SentencePolarity'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license="MIT",        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'SentencePolarity in python 3',   # Give a short description about your library
  author = 'claire',                   # Type in your name
  author_email = 'claire.malbrel@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/clairemalbrel/SentencePolarity',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/clairemalbrel/SentencePolarity/archive/field.tar.gz',    # I explain this later on
  keywords = ['sentiment', 'score', 'analysis'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
          'gcsfs==0.6.0',
            'google-cloud-storage==1.26.0',
            'pandas==0.24.2',
            'stemming',
            'nltk',
            'setuptools',
            'scrapy',
            'vaderSentiment',
            'scikit-learn'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)

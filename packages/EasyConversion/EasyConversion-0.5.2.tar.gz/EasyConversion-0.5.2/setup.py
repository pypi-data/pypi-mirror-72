from distutils.core import setup
long_description="""
A python package for easily converting between python and decimal. Mostly a test of packaging. This is an early project so there may be bugs.
 | 0.4.0 - Big update. Please see https://easyconversion.readthedocs.io/en/latest/#version-history for more.
 | 0.4.1 - Patches for 0.4.0
 | 0.5.0 - Many new changes! See https://easyconversion.readthedocs.io/en/latest/#version-history for changelogs
 | 0.5.1 - Small fixes and changes
 | 0.5.2 - New error message changes 
"""
setup(
  name = 'EasyConversion',         # How you named your package folder (MyLib)
  packages = ['EasyConversion'],   # Chose the same as "name"
  version = '0.5.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Easily converting in python (alpha)',   # Give a short description about your library
  long_description=long_description,
  author = 'Coolo2',                   # Type in your name
  author_email = 'itsxcoolo2@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Coolo22/EasyConversion',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Coolo2/EasyConversion/archive/v_050.tar.gz',    # I explain this later on
  keywords = ['Decimal', 'Binary', 'ascii', 'morse', 'Convert'],   # Keywords that define your package best
  install_requires=[],
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
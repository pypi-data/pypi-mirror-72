#!/usr/bin/env python

from distutils.core import setup

setup( name                 = 'coreframe',
       version              = '0.1a',
       description          = 'COmmon REsearch FRAMEwork',
       long_description     = ''' long_description to be written. ''',
       classifiers          = [
                            'Development Status :: 4 - Beta',
                            'License :: OSI Approved :: MIT License',
                            'Programming Language :: Python :: 2.7',
                            'Topic :: Scientific/Engineering :: Atmospheric Science',
                            ],
       keywords             = '',
       url                  = 'https://github.com/hyungjun/coreframe',
       author               = 'Hyungjun Kim',
       author_email         = 'hyungjun@gmail.com',
       license              = 'MIT',

       package_dir          = {'TimeSeries':''},
       packages             = ['TimeSeries',],
      )


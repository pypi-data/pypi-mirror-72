
from setuptools import setup
setup(
  name = 'swan_vis',
  packages = ['swan_vis'],
  version = 'v1.0.2',
  license='MIT',  description = 'swan is a tool for visualizing and analyzing transcript isoforms',
  author = 'Fairlie Reese',
  author_email = 'fairlie.reese@gmail.com',
  url = 'https://github.com/mortazavilab/swan_vis/',
  download_url = 'https://github.com/mortazavilab/swan_vis/archive/v1.0.2.tar.gz',
  keywords = ['swan', 'transcription', 'isoform', 'visualization'],
  install_requires=[
          'networkx',
          'numpy',
          'pandas',
          'matplotlib',
          'fpdf',
          'seaborn',
          'diffxpy',
          'tensorflow',
          'tensorflow-probability',
	        'pathlib'
    ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research ',    
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
  ],
      entry_points={
        "console_scripts": [
            'swan_patch_networkx=swan_vis.networkx_patch:main'
        ]
    }
)

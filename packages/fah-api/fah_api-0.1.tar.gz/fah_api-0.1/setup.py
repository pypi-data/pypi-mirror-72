from distutils.core import setup
setup(
  name = 'fah_api',
  packages = ['fah_api'],
  version = '0.1',
  license='MIT',
  description = 'A python3 library for controlling Folding@Home clients',
  author = 'Ben Cordes',
  author_email = 'cordes.ben@gmail.com',
  url = 'https://github.com/fraterrisus/fah-api-python',
  download_url = 'https://github.com/fraterrisus/fah-api-python/archive/v0.1.tar.gz',
  keywords = ['foldingathome'],
  install_requires=[],
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: End Users/Desktop',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Software Development :: Libraries',
    'Topic :: Home Automation',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)

from setuptools import setup


setup(
  name         = 'HermesCache',
  version      = '0.8.0',
  author       = 'saaj',
  author_email = 'mail@saaj.me',
  packages     = ['hermes', 'hermes.backend', 'hermes.test'],
  url          = 'https://heptapod.host/saajns/hermes',
  license      = 'LGPL-2.1+',
  description  = (
    'Python caching library with tag-based invalidation and dogpile effect prevention'
  ),
  long_description = open('README.rst', 'rb').read().decode('utf-8'),
  platforms        = ['Any'],
  python_requires  = '>= 3',
  keywords         = 'python cache tagging redis memcached',
  classifiers      = [
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: Implementation :: CPython',
    'Intended Audience :: Developers',
  ],
  extras_require = {
    'redis'         : ['redis'],
    'redis-ext'     : ['redis', 'hiredis'],
    'memcached'     : ['python3-memcached'],
    'memcached-ext' : ['pylibmc >= 1.4'],
  },
)


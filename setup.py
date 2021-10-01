# bootstrap if we need to
try:
    import setuptools  # noqa
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages

classifiers = ['Development Status :: 3 - Alpha',
               'Environment :: Console',
               'Intended Audience :: Developers',
               'Intended Audience :: End Users/Desktop',
               'Intended Audience :: Other Audience',
               'Natural Language :: English',
               'Operating System :: MacOS :: MacOS X',
               'Operating System :: Microsoft :: Windows',
               'Operating System :: POSIX',
               'Programming Language :: Python :: 3.8',
               'Programming Language :: Python :: Implementation :: CPython',
               'Topic :: Communications :: Chat',
               ]

setup(author='Code-in-public contributors',
      author_email='code-in-public',
      classifiers=classifiers,
      description='allow twitch viewers to cause chaos',
      name='streamchaos',
      url='http://github.com/code-in-public/streamchaos',
      packages=find_packages(),
      entry_points={'console_scripts': ['streamchaos = streamchaos:main']},
      version='0.1.0',
      install_requires=['click', 'dotenv', 'twitchapi'],
      zip_safe=False,
      )

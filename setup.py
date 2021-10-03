try:
    import setuptools  # noqa
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
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

setup(
    name='StreamChaos',
    version='0.1.0',
    description='Allow twitch viewers to cause chaos',
    url='http://github.com/code-in-public/streamchaos',
    author='twitch.tv/codeinpublic Community',
    author_email='',
    classifiers=classifiers,
    entry_points={'console_scripts': ['streamchaos = streamchaos.cli:main']},
    install_requires=['click', 'python-dotenv', 'twitchapi', 'wheel'],
    packages=find_packages(),
    zip_safe=False
)

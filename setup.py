import re
from distutils.core import setup


def get_version(version_file):
    pattern = r"^__version__ = ['\"]([^'\"]*)['\"]"
    match = re.search(pattern, open(version_file, "rt").read(), re.MULTILINE)
    if match:
        return match.group(1)

    raise RuntimeError("Unable to find version string in %s." % (version_file,))


setup(name='pydateinfer',
      version=get_version("dateinfer/__init__.py"),
      description='Infers date format from examples',
      long_description="""Uses a series of pattern matching and rewriting rules to compute a "best guess" datetime.strptime format string give a list of example date strings.""",
      author='Jeffrey Starr',
      author_email='will@pedalwrencher.com',
      url='https://github.com/nedap/dateinfer',
      packages=['dateinfer'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      install_requires=['pytz']
      )

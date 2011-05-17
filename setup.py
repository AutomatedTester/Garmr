import os
import sys
from setuptools import setup, find_packages
def main():
    setup(name='Garmr',
          version='0.1a',
          description='A tool for testing a web application for basic security holes',
          author='David Burns',
          author_email='dburns at mozilladotcom',
          entry_points= make_entry_points(),
          url='https://github.com/AutomatedTester/Garmr',
          classifiers=['Development Status :: 2 - Pre-Alpha',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Software Development :: Testing',
                     'Topic :: Software Development :: Libraries',
                     'Programming Language :: Python'],
        packages=find_packages()
)

def cmdline_entrypoints(versioninfo, platform, basename):
    target = 'garmr:main'
    if platform.startswith('java'):
        points = {'garmr': target}
    else:
        if basename.startswith("pypy"):
            points = {'garmr-%s' % basename: target}
        else: # cpython
            points = {'garmr-%s.%s' % versioninfo[:2] : target,}
        points['garmr'] = target
    return points

def make_entry_points():
    basename = os.path.basename(sys.executable)
    points = cmdline_entrypoints(sys.version_info, sys.platform, basename)
    keys = list(points.keys())
    keys.sort()
    l = ["%s = %s" % (x, points[x]) for x in keys]
    return {'console_scripts': l}

if __name__ == '__main__':
    main()

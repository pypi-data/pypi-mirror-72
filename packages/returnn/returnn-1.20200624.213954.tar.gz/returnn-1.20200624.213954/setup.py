

"""
Usage:

Create ~/.pypirc with info:

    [distutils]
    index-servers =
        pypi

    [pypi]
    repository: https://upload.pypi.org/legacy/
    username: ...
    password: ...

(Not needed anymore) Registering the project: python3 setup.py register
New release: python3 setup.py sdist upload

I had some trouble at some point, and this helped:
pip3 install --user twine
python3 setup.py sdist
twine upload dist/*.tar.gz

See also MANIFEST.in for included files.

For debugging this script:

python3 setup.py sdist
pip3 install --user dist/*.tar.gz -v
(Without -v, all stdout/stderr from here will not be shown.)

"""

from __future__ import print_function
import time
from pprint import pprint
import os
import sys
from subprocess import Popen, check_output, PIPE


_my_dir = os.path.dirname(os.path.abspath(__file__))


def debug_print_file(fn):
  """
  :param str fn:
  """
  print("%s:" % fn)
  if not os.path.exists(fn):
    print("<does not exist>")
    return
  if os.path.isdir(fn):
    print("<dir:>")
    pprint(sorted(os.listdir(fn)))
    return
  print(open(fn).read())


def parse_pkg_info(fn):
  """
  :param str fn:
  :rtype: dict[str,str]
  """
  res = {}
  for ln in open(fn).read().splitlines():
    if not ln or not ln[:1].strip():
      continue
    key, value = ln.split(": ", 1)
    res[key] = value
  return res


def git_commit_rev(commit="HEAD", git_dir="."):
  """
  :param str commit:
  :param str git_dir:
  :rtype: str
  """
  if commit is None:
    commit = "HEAD"
  return check_output(["git", "rev-parse", "--short", commit], cwd=git_dir).decode("utf8").strip()


def git_is_dirty(git_dir="."):
  """
  :param str git_dir:
  :rtype: bool
  """
  proc = Popen(["git", "diff", "--no-ext-diff", "--quiet", "--exit-code"], cwd=git_dir, stdout=PIPE)
  proc.communicate()
  if proc.returncode == 0:
    return False
  if proc.returncode == 1:
    return True
  raise Exception("unexpected return code %i" % proc.returncode)


def git_commit_date(commit="HEAD", git_dir="."):
  """
  :param str commit:
  :param str git_dir:
  :rtype: str
  """
  out = check_output(["git", "show", "-s", "--format=%ci", commit], cwd=git_dir).decode("utf8")
  out = out.strip()[:-6].replace(":", "").replace("-", "").replace(" ", ".")
  return out


def git_head_version(git_dir="."):
  """
  :param str git_dir:
  :rtype: str
  """
  commit_date = git_commit_date(git_dir=git_dir)  # like "20190202.154527"
  # rev = git_commit_rev(git_dir=git_dir)
  # is_dirty = git_is_dirty(git_dir=git_dir)
  # Make this distutils.version.StrictVersion compatible.
  return "1.%s" % commit_date


def get_version_str(verbose=False, allow_current_time=False, fallback=None):
  """
  :param bool verbose:
  :param bool allow_current_time:
  :param str|None fallback:
  :rtype: str
  """
  if os.path.exists("%s/PKG-INFO" % _my_dir):
    if verbose:
      print("Found existing PKG-INFO.")
    info = parse_pkg_info("%s/PKG-INFO" % _my_dir)
    version = info["Version"]
    if verbose:
      print("Version via PKG-INFO:", version)
  else:
    try:
      version = git_head_version()
      if verbose:
        print("Version via Git:", version)
    except Exception as exc:
      if verbose:
        print("Exception while getting Git version:", exc)
        sys.excepthook(*sys.exc_info())
      if allow_current_time:
        version = time.strftime("1.%Y%m%d.%H%M%S", time.gmtime())
        if verbose:
          print("Version via current time:", version)
      else:
        if fallback:
          return fallback
        raise
  return version


def main():
  """
  Setup main entry
  """
  version = get_version_str(verbose=True, allow_current_time=True)

  if os.environ.get("DEBUG", "") == "1":
    debug_print_file(".")
    debug_print_file("PKG-INFO")
    debug_print_file("pip-egg-info")
    debug_print_file("pip-egg-info/returnn.egg-info")
    debug_print_file("pip-egg-info/returnn.egg-info/SOURCES.txt")  # like MANIFEST

  if os.path.exists("PKG-INFO"):
    if os.path.exists("MANIFEST"):
      print("package_data, found PKG-INFO and MANIFEST")
      package_data = open("MANIFEST").read().splitlines() + ["PKG-INFO"]
    else:
      print("package_data, found PKG-INFO, no MANIFEST, use *")
      # Just using package_data = ["*"] would only take files from current dir.
      package_data = []
      for root, dirs, files in os.walk('.'):
        for file in files:
          package_data.append(os.path.join(root, file))
  else:
    print("dummy package_data, does not matter, likely you are running sdist")
    package_data = ["MANIFEST"]

  from distutils.core import setup
  setup(
    name='returnn',
    version=version,
    packages=['returnn'],
    package_dir={'returnn': ''},
    package_data={'returnn': package_data},  # filtered via MANIFEST.in
    description='The RWTH extensible training framework for universal recurrent neural networks',
    author='Albert Zeyer',
    author_email='albzey@gmail.com',
    url='https://github.com/rwth-i6/returnn/',
    license='RETURNN license',
    long_description=open('README.rst').read(),
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'Intended Audience :: Education',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: BSD License',
      'Operating System :: MacOS :: MacOS X',
      'Operating System :: Microsoft :: Windows',
      'Operating System :: POSIX',
      'Operating System :: Unix',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
    ]
  )


if __name__ == "__main__":
  main()

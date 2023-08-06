from setuptools import setup, find_packages, Distribution
import codecs
import os.path

# Make sure versiontag exists before going any further
Distribution().fetch_build_eggs('versiontag')

from versiontag import get_version, cache_git_tag  # NOQA


packages = find_packages('src')

install_requires = [
    'Django>=2.2',
    'django-ipware>=3.0.0,<4.0.0',
]

extras_require = {
    'development': [
        'flake8>=3.2.1',
        'freezegun>=0.3.10',
    ],
}



def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()


cache_git_tag()

setup(
    name="django-auth-logger",
    description="A tiny project to log login attempts. Log them only to standard logging - not the database.",
    version=get_version(pypi=True),
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    author="David Burke",
    author_email="david@thelabnyc.com",
    url='https://gitlab.com/thelabnyc/django-auth-logger',
    license="ISC",
    package_dir={'': 'src'},
    packages=packages,
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
)

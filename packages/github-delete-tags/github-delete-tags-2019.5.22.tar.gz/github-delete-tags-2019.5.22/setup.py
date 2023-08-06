try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='github-delete-tags',
    version='2019.5.22',
    scripts=[
        'scripts/github-delete-tags',
    ],
)

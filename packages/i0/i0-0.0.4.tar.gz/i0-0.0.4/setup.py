from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='i0',
    version='0.0.4',
    description='Simple data service.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/0oio/i0',
    author='Mindey',
    author_email='~@mindey.com',
    license='MIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'fastapi[all]',
        'typer',
        'metaform',
        'metatype',
        'feedparser', # cause yaml restores python types..
        'PyRSS2Gen',
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'i0=i0.main:cli',
            'i0o=i0.main:packmaker'
        ],
    }
)

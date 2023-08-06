from distutils.core import setup

setup(
    name='distcache',
    version='0.1.1',
    author='wasim akram khan',
    keywords='open-source, cache, distributed-cache, in-memory, database',
    description='Distcache is a python open-source distributed in-memory cache and database.',
    packages=['distcache', 'usage', 'benchmark', 'tests'],
    license='MIT License ',
    long_description=open('pypi_readme.md').read(),
    project_urls={
        "Source Code": "https://github.com/wasimusu/distcache",
    },
)

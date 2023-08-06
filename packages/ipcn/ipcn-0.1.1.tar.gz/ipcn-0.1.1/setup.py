import re

from setuptools import find_packages, setup

extras_require = {}

version = None
with open('ipcn/__init__.py', 'r') as f:
    for line in f:
        m = re.match(r'^__version__\s*=\s*(["\'])([^"\']+)\1', line)
        if m:
            version = m.group(2)
            break
setup(
    name="ipcn",
    version=version,
    description="IP utilities",
    author='plusplus1',
    author_email='pror885@163.com',
    url='https://github.com/plusplus1/ipcn',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests>=2.22.0",
        "diskcache>=2.4.1",
    ],
    entry_points="""
    [console_scripts]
    ipcn=ipcn.run:main
    """,
    extras_require=extras_require,
)

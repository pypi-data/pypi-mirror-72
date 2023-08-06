from setuptools import find_packages, setup

extras_require = {}

__version__ = '0.1.2'

setup(
    name="ipcn",
    version=__version__,
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
        "diskcache>=4.1.0",
    ],
    entry_points={
        'console_scripts': [
            'ipcn=ipcn.run:main'
        ]
    },
    extras_require=extras_require,
)

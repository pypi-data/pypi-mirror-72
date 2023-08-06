# Always prefer setuptools over distutils
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

install_requires = [
]
setup(
    name='dmz',
    version='0.9.0',
    description='DMZ proxy',

    # The project's main homepage.
    url='https://gitee.com/rushmore/dmz',

    # Author details
    author='Rushmore (Leiming Hong)',
    author_email='hong.leiming@qq.com',

    # Choose your license
    license='LGPL',

    classifiers=[
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.7',
    ],
    include_package_data=True,
    install_requires=install_requires,
    keywords='dmz,proxy',
    packages=find_packages()
)

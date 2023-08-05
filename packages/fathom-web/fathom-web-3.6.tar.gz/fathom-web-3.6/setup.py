from io import open
from setuptools import setup, find_packages


setup(
    name='fathom-web',
    version='3.6',
    description='Commandline tools for training Fathom rulesets',
    long_description=open('README.rst', 'r', encoding='utf8').read(),
    author='Erik Rose',
    author_email='erik@mozilla.com',
    license='MPL',
    packages=find_packages(exclude=['*.test']),
    url='https://mozilla.github.io/fathom/',
    install_requires=[
        'click>=7.0,<8.0',
        'more-itertools>=8.2,<9.0',
        'numpy>=1.18.1,<2.0',
        'filelock>=3.0.12',
        'scikit-learn>=0.22.2',
        'selenium>=3.141.0',
        'tensorboardX>=1.6,<2.0',
        'torch>=1.0,<2.0'
    ],
    dependency_links=[
        'https://download.pytorch.org/whl/torch_stable.html'
    ],
    entry_points={'console_scripts': [
        'fathom-extract = fathom_web.commands.extract:main',
        'fathom-fox = fathom_web.commands.fox:main',
        'fathom-histogram = fathom_web.commands.histogram:main',
        'fathom-label = fathom_web.commands.label:main',
        'fathom-list = fathom_web.commands.list:main',
        'fathom-pick = fathom_web.commands.pick:main',
        'fathom-serve = fathom_web.commands.serve:main',
        'fathom-test = fathom_web.commands.test:main',
        'fathom-train = fathom_web.commands.train:main',
    ]},
    package_data={'': ['fathom.zip']},
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3'
    ],
    keywords=['machine learning', 'ml', 'semantic extraction'],
)

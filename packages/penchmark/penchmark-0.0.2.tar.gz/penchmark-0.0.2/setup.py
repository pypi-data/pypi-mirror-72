import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

VERSION = '0.0.2'

setuptools.setup(
    name='penchmark',
    version=VERSION,
    author='Ruslan Zaporojets',
    author_email='ruzzzua@gmail.com',
    description='Python code benchmark library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['benchmark'],
    url='https://github.com/ruzzz/penchmark',
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Benchmark',
        'Topic :: Utilities'
    ],
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md"],
    },
    python_requires='>=3.6',
    install_requires=[
        'tabulate>=0.8.7'
    ],
    extras_require={
        'dev': [
            'mypy>=0.782',
            'pylint>=2.5.3',
            'pylint-quotes>=0.2.1',
            'pytest>=5.4.3',
            'pytest-cov>=2.10.0'
        ],
        'charts': [
            'matplotlib>=3.2.2',
            'pandas>=1.0.5',
            'seaborn>=0.10.1'
        ]
    }
)

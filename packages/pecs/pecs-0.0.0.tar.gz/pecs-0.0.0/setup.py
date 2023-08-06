from setuptools import setup
from setuptools import find_packages
from src.pecs import VERSION

setup(
    name='pecs',
    version=VERSION,
    description='A type-safe, customizable DAO generator for Python 3 connecting to PostgreSQL',
    long_description='TBA',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Database :: Front-Ends',
    ],
    keywords='python sql dao dal generator',
    author='Eric Borczuk',
    author_email='kuzcrob@gmail.com',
    url='https://github.com/EricBorczuk/pecs',
    project_urls={'Issues': 'https://github.com/EricBorczuk/pecs/issues'},
    license='MIT',
    package_dir={"": "src"},
    packages=find_packages('src', exclude=['examples*', 'test*']),
    # install_requires=[], # TODO add in other dependencies
    entry_points={'console_scripts': ['pecs = pecs.__main__:main']},
)

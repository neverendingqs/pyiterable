from setuptools import setup

setup(
    name='pyiterable',
    version='0.4.0',
    description='Iterable chains',
    long_description='Write more expressive code by chaining built-in transformations together.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    url='https://github.com/neverendingqs/pyiterable',
    author='neverendingqs',
    author_email='mark.tse@neverendingqs.com',
    license='MIT',
    packages=['pyiterable'],
    test_suite='nose.collector',
    tests_require=['nose', 'unittest2'],
    zip_safe=False
)

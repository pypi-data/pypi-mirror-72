from setuptools import setup, find_packages

setup(
    name='kotev',
    version='0.0.1',
    description='Tool for working with the Hebrew alphabet',
    long_description=open("README.rst").read(),
    keywords='natural_language',
    author='JJ Ben-Joseph',
    author_email='jj@memoriesofzion.com',
    python_requires='>=3.8',
    url='https://www.github.com/bnext-iqt/corona-dashboard',
    license='Apache',
    classifiers=[
        'Natural Language :: Hebrew',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent'
    ],
    packages=find_packages(),
    install_requires=['fire'],
    entry_points={
        'console_scripts': [
            'kotev = kotev.__main__:main',
        ],
    },
)


# python
import pathlib
import setuptools

THIS_DIR = pathlib.Path(__file__).parent.absolute()

with open(str(THIS_DIR/'README.md')) as f:
    long_description = f.read()
    
_repromancy = setuptools.Extension('_repromancy', sources = ['_repromancy.c'])

setuptools.setup(
    name='repromancy',
    version='0.0.1',
    author='Erik Soma',
    author_email='stillusingirc@gmail.com',
    description='Utilize dark magic to unify reprs.',
    tests_require=['pytest'],
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/esoma/repromancy',
    packages=setuptools.find_packages(exclude='test'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    ext_modules=[_repromancy],
)

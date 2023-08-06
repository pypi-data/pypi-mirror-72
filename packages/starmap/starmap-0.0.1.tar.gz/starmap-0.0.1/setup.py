import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='starmap',
    version='0.0.1',
    author='Chris Roat',
    author_email='croat@stanford.edu',
    description='StarMap placeholder',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/deisseroth-lab/starmap',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

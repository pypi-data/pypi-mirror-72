import setuptools

with open('README.md', 'r') as stream:
    LONG_DESCRIPTION = stream.read()

with open('LICENSE', 'r') as stream:
    LICENSE = stream.read()

setuptools.setup(
    name='scrapy-coco',
    version='0.1.1',
    author='Giorgi Jambazishvili (m3ck0)',
    author_email='m3ck0@pm.me',
    description='Micro scraper framework',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/pypa/sampleproject',
    packages=setuptools.find_packages(exclude=('test',)),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    license=license,
    install_requires=(
        'aiohttp',
        'beautifulsoup4',
        'lxml'
    )
)
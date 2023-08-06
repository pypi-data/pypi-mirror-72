import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('VERSION', 'r') as f:
    version = f.readline().strip()

setuptools.setup(
    name='f-codec',
    version=version,
    author='Vitaly Kravtsov',
    author_email='in4lio@gmail.com',
    description="Python 'f' Codec",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/in4lio/f-codec',
    packages=['fcodec'],
    data_files=[('lib/python/site-packages', ['fcodec.pth'])],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    platforms='any',
    python_requires='>=3.6',
)

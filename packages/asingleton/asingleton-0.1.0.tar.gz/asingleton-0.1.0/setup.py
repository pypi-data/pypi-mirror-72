import setuptools

import asingleton


setuptools.setup(
    name='asingleton',
    version=asingleton.__version__,
    author=asingleton.__author__,
    author_email='guallo.username@gmail.com',
    description='singleton(cls, '
                            '[attr_name,] '
                            '[disable_name_mangling,] '
                            '[not_just_this_class,]) is cls',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/guallo/asingleton',
    packages=[asingleton.__name__],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

from setuptools import setup, find_packages

setup(
    name = 'comake',
    packages=find_packages(), # this must be the same as the name above
    version = 'v0.1.6',
    description = 'A c++ build tool',
    author = 'liaosiwei',
    author_email = 'liaosiwei@163.com',
    url = 'https://github.com/boully/comake',
    download_url = 'https://github.com/boully/comake/tarball/v0.1.6',
    keywords = ['c++', 'auto-build', 'dependency'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        "GitPython",
        "pytoml",
        "Jinja2",
    ],
    entry_points={
        'console_scripts': [
            'comake=comake.Comake:main',
        ],
    },
)

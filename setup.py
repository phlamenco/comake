from distutils.core import setup
setup(
    name = 'comake',
    packages = ['comake'], # this must be the same as the name above
    version = 'v0.1.0',
    description = 'A c++ build tool',
    author = 'liaosiwei',
    author_email = 'liaosiwei@163.com',
    url = 'https://github.com/boully/comake', # use the URL to the github repo
    download_url = 'https://github.com/boully/comake/tarball/v0.1.0', # I'll explain this in a second
    keywords = ['c++', 'auto-build', 'dependency'], # arbitrary keywords
    classifiers = [],
)

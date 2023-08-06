
SETUP_INFO = dict(
    name = 'infi.ramen_client',
    version = '1.40.post3',
    author = 'Itay Galea',
    author_email = 'igalea@infinidat.com',

    url = 'https://git.infinidat.com/host-internal/infi.ramen_client',
    license = 'PSF',
    description = """A client library for sending data to Ramen.""",
    long_description = """A client library for sending data to Ramen.""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'future',
'requests',
'schematics',
'setuptools',
'six'
],
    namespace_packages = ['infi'],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()


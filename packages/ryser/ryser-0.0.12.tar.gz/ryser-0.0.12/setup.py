from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = 'ryser',
    version = '0.0.12',
    packages = ['ryser',],
    description = "Latin squares and related designs.",
    author = "Matthew Henderson",
    author_email = "matthew.james.henderson@gmail.com",
    url = "http://packages.python.org/ryser/",
    download_url = "http://pypi.python.org/pypi/ryser/",
    keywords = [""],
    classifiers = [
        "Programming Language :: Python",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    license = 'LICENSE.txt',
    long_description = readme(),
    test_suite='nose.collector',
    tests_require=['nose'],
)


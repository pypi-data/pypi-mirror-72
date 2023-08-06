from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
# with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()

packages = ['pillow_tools']
print('packages=', packages)

setup(
    name="pillow_tools",

    version="1.0.0",
    # 1.0.0 - init release to pypi

    packages=packages,
    install_requires=['pillow', 'ffmpy'],
    # scripts=['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    # install_requires=['docutils>=0.3'],

    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst'],
    #     # And include any *.msg files found in the 'hello' package, too:
    #     'hello': ['*.msg'],
    # },

    # metadata to display on PyPI
    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="A collection of useful tools for python pillow and ffmpy",
    long_description="A collection of useful tools for python pillow and ffmpy",
    license="PSF",
    keywords="grant miller pillow ffmpeg ffmpy image video",
    url="https://github.com/GrantGMiller/gm_pillow_tools",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/gm_pillow_tools",
    }

    # could also include long_description, download_url, classifiers, etc.
)

# to push to PyPI

# python -m setup.py sdist bdist_wheel
# twine upload dist/*
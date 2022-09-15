import setuptools

import pymnk

with open("README.md", "r", encoding='utf-8') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name="pymnk",
    version=pymnk.__version__,
    author=pymnk.__author__,
    description="Python library for k-in-a-row family of games, including\
    (m,n,k)-game, Connect6, Pente, Ultimate tic-tac-toe and others",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ZetaFactorial/pymnk",
    license="MIT",
    keywords='tictactoe tic-tac-toe gomoku connect6 pente',
    packages=setuptools.find_packages(),
    zip_safe=False,
    package_data={"pymnk": ["py.typed"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    project_urls={
        'Source': 'https://github.com/ZetaFactorial/pymnk',
        'Tracker': 'https://github.com/ZetaFactorial/pymnk/issues',
    },
)
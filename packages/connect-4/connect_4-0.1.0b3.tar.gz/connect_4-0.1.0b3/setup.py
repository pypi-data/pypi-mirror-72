import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="connect_4",
    version="0.1.0-beta.3",
    author="Ritwik G",
    author_email="i@ritwikg.com",
    description="A connect 4 CLI game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ritwikgopi/connect-4",
    packages=setuptools.find_packages(include=("connect_4",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "connect_4 = connect_4.game_engine:main"
        ]
    },
    python_requires='>=3.6',
)

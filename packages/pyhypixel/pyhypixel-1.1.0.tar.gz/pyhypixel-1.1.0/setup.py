# A Python3 HypixelAPI wrapper
#     Copyright (C) 2020  Michele Viotto

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
import setuptools


with open("README.md", "r") as file:
    long_desc = file.read()


setuptools.setup(
    name="pyhypixel",
    version="1.1.0",
    author="SonoMichele",
    author_email="micheleviotto@protonmail.com",
    description="An unofficial HypixelAPI wrapper",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/xMicky24GIT/pyhypixel",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)

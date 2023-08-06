import setuptools
import re


def get_requirements():
    reqs = []
    for line in open('requirements.txt', 'r').readlines():
        reqs.append(line)
    return reqs

# auto-updating version code stolen from Orbitize(stolen from RadVel) :)


def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
                       open(project + '/__init__.py').read())
    return result.group(1)


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="percolation-threshold",
    version=get_property('__version__', 'percolation'),
    author="MissingBrainException, Khadir Mohamed Islam, Abdennour Slimane",
    author_email="muhammad.masud.1997@gmail.com, islam.islam.khadir6@gmail.com, slimaneabdennourphysics@gmail.com",
    description="Computational tool to calculate percolation threshold for various lattices",
    install_requires=get_requirements(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MissingBrainException/PercolationThreshold",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    python_requires='>=3.3',
)

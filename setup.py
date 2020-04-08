import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_requirements(file):
    with open(file, "r") as f:
        return f.readlines()


install_requires = read_requirements("requirements.txt")
dev_requires = read_requirements("requirements-dev.txt")
test_requires = read_requirements("requirements-test.txt")
extras = {
    'test': test_requires,
    'dev' : dev_requires
}

setuptools.setup(
    name="jenkinscli",
    use_scm_version=True,
    author="Kazuhiro Suzuki",
    author_email="ksauzzmsg@gmail.com",
    description="Jenkins CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ksauzz/jenkinscli",
    packages=setuptools.find_packages(),
    setup_requires=['setuptools_scm'],
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require=extras,
    scripts=['bin/jenkinscli'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
)

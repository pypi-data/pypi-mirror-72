import setuptools

setuptools.setup(
    name='travis-env',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

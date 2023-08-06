import setuptools

setuptools.setup(
    name='pypi-simple-iter',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

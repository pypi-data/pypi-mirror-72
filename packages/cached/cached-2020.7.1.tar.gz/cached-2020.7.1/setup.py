import setuptools

setuptools.setup(
    name='cached',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

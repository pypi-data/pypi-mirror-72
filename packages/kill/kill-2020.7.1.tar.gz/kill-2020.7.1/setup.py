import setuptools

setuptools.setup(
    name='kill',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

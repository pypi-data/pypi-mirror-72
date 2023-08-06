import setuptools

setuptools.setup(
    name='getdirs',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

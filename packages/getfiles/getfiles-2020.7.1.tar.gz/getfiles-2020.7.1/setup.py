import setuptools

setuptools.setup(
    name='getfiles',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

import setuptools

setuptools.setup(
    name='columnate',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

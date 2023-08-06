import setuptools

setuptools.setup(
    name='format-keys',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

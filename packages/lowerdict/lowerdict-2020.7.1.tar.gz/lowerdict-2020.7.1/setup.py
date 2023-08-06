import setuptools

setuptools.setup(
    name='lowerdict',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

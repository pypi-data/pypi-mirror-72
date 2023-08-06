import setuptools

setuptools.setup(
    name='rmdir',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

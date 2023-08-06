import setuptools

setuptools.setup(
    name='git-status',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

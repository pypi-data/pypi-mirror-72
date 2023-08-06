import setuptools

setuptools.setup(
    name='jsfiddle-github',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

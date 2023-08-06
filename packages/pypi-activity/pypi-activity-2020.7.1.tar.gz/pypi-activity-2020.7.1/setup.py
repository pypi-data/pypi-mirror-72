import setuptools

setuptools.setup(
    name='pypi-activity',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

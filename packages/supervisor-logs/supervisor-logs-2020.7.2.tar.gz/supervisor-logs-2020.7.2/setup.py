import setuptools

setuptools.setup(
    name='supervisor-logs',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

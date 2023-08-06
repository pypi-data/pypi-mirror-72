import setuptools

setuptools.setup(
    name='growlnotify',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

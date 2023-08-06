import setuptools

setuptools.setup(
    name='mac-speech-commands',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

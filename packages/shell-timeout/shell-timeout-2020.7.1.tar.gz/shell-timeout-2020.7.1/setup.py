import setuptools

setuptools.setup(
    name='shell-timeout',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages(),
    scripts=['scripts/timeout']
)

import setuptools

setuptools.setup(
    name='django-context-extra-view',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

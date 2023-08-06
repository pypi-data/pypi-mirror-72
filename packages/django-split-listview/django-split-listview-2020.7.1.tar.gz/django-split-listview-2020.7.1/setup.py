import setuptools

setuptools.setup(
    name='django-split-listview',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

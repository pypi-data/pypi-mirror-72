import setuptools

setuptools.setup(
    name='django-replace',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

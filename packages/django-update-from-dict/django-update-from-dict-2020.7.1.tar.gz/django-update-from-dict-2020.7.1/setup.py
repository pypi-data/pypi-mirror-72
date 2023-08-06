import setuptools

setuptools.setup(
    name='django-update-from-dict',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

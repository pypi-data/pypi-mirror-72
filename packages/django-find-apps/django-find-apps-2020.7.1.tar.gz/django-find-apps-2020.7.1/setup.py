import setuptools

setuptools.setup(
    name='django-find-apps',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

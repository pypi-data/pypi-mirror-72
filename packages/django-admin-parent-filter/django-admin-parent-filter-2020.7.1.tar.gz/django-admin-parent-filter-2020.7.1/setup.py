import setuptools

setuptools.setup(
    name='django-admin-parent-filter',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)

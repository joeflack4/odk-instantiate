"""Setup"""
from setuptools import setup, find_packages


from pmix import __version__

pkg_name = 'odk_instantiate'
packages = find_packages(exclude=['test'])
packages.append(pkg_name+'.test')

setup(
    name='odk_instantiate',
    version=__version__,
    author='Joseph Eugene Flack IV',
    author_email='joeflack4@gmail.com',
    url='http://www.pma2020.org',
    packages=packages,
    package_dir={
        pkg_name+'.test': 'test'
    },
    package_data={
        pkg_name+'.test': [
            'files/*.xlsx',
            'files/templates/*.xlsx'
        ],
    },
    license='LICENSE.txt',
    description='A build tool for creating ODK XlsForms from generic reference'
                ' Excel templates.',
    long_description=open('README.md').read(),
    install_requires=[

    ],
)

from setuptools import setup
from setuptools import find_packages


classifiers = [
    'License :: OSI Approved :: MIT License',
    'Development Status :: 4 - Beta',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3 :: Only',
    'Operating System :: POSIX',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
    'Framework :: AsyncIO',
]

install_requires = [
    "aiohttp>=3.6.2",
    "babel>=2.7.0",
]
tests_require = [
    "mypy>=0.740",
    "pytest>=5.3.0",
    "pytest-cov>=2.8.1",
    "pyfakefs>=3.6.1",
    "pytest-mock>=1.12.1",
    "pytest-aiohttp>=0.3.0",
    "flake8",
]

setup(
    name="aiohttp-i18n",
    version="0.0.7",
    packages=find_packages(),
    python_requires='>=3.7',
    extras_require={
        'test': tests_require,
    },
    install_requires=install_requires,
    author="Vitalii Mazur",
    author_email="vitalii.mazur@gmail.com",
    platforms=["POSIX"],
    description="i18n support for aiohttp through babel",
    classifiers=classifiers,
    license="MIT",
    include_package_data=True,
    keywords="aiohttp i18n locale babel localization",
    url="https://bitbucket.org/mazvv/aiohttp_i18n",
)

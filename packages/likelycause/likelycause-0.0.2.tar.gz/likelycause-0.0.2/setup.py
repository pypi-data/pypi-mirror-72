import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Ana Garcia",
    author_email="ana.n.garcia2@gmail.com",
    name='likelycause',
    license="MIT",
    description='Likely cause finds creative ways to identify causes',
    version='v0.0.2',
    long_description=README,
    url='https://github.com/shaypal5/chocobo',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=['warnings','scipy',
    'sklearn','statsmodels'],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)

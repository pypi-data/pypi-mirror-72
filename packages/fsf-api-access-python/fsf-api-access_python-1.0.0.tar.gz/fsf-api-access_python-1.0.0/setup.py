from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = [x.strip() for x in f.readlines()]

with open('extra_test_requires.txt') as f:
    extra = {'testing': [x.strip() for x in f.readlines()]}

setup(
    name='fsf-api-access_python',
    version='1.0.0',
    description='A Python API Access Client for the First Street Foundation API',
    url='https://github.com/FirstStreet/fsf_api_access_python',
    project_urls={
        'First Street Foundation Website': 'https://firststreet.org/'
    },
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Kelvin",
    author_email="kelvin@firststreet.org",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],

    # Package info
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    py_modules=[],
    install_requires=requirements,
    python_requires='>=3.6',
    extras_require=extra
)

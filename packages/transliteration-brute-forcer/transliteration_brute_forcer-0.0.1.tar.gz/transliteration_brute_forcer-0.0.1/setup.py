from setuptools import setup, find_packages

classifiers = [
    'License :: OSI Approved :: MIT License',
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Intended Audience :: Developers',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
]

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='transliteration_brute_forcer',
    version='0.0.1',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=classifiers,
    author='Alexander Karateev',
    author_email='administrator@gintr1k.space',
    url='https://github.com/GinTR1k/Transliteration-BruteForcer',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
)

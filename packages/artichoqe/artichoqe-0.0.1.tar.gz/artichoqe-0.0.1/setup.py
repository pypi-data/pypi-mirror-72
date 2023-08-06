import setuptools
from setuptools import setup

TEST_DEPS = [
    'mock==3.0.5',
    'pytest==5.0.1',
    'pytest-runner==5.1',
    'pytest-pylint==0.14',
    'pytest-cov==2.7.1',
    'pylint==2.3.1',
]

setup(
    name='artichoqe',
    author='Unfeatured team',
    version='0.0.1',
    author_email='noreply@lost.com',
    url='https://github.com/vmdude/artichoqe',
    download_url='https://github.com/vmdude/artichoqe/archive/0.0.1.tar.gz',
    description='Artichoqe is a cloud metadata collector, helping you in your daily decision',
    long_description='file: README.md',
    license='WTFPL',
    keywords='aws, prometheus, cloudformation',
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ],
    entry_points={
        'console_scripts': ['artichoqe=artichoqe.main:main']
    },
    zip_safe=True,
    include_package_data=True,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'boto==2.49',
        'boto3==1.10.46',
        'yamllint==1.20.0',
        'Jinja2==2.10.3',
        'click==7.0',
        'docker==4.0.2'
    ],
    tests_require=TEST_DEPS,
    extras_require={
        'test': TEST_DEPS
    }
)

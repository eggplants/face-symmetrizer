from setuptools import find_packages, setup  # type: ignore

setup(
    name='face_symmetrizer',
    version='1.4',
    description='Easy symmetrizer for an image contained face(s)',
    description_content_type='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eggplants/face-symmetrizer',
    author='eggplants',
    packages=find_packages(),
    python_requires='>=3.8',
    include_package_data=True,
    license='MIT',
    install_requires=open('requirements.txt').read().rstrip().split('\n'),
    entry_points={
        'console_scripts': [
            'fsym=face_symmetrizer.main:main'
        ]
    }
)

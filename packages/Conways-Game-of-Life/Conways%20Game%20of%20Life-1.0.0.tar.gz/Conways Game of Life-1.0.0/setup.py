import os 
from setuptools import setup

def readme_file():
    readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.rst')

    with open(readme_path) as r:
        file_content = r.read()
    return file_content


setup(
        name='Conways Game of Life',
        version='1.0.0',
        description='Build week project for CS30 at Lambda School',
        long_description=readme_file(),
        license='MIT',
        author='Yoni Pineda',
        author_email='yonipineda1010@icloud.com',
        url='https://github.com/Yonipineda/Conways-GameOfLife',
        download_url='https://github.com/Yonipineda/Conways-GameOfLife/archive/v_1.0.0.tar.gz',
        script=['2-Player/ConwaysGameOfLife.py'],
        zip_safe=False,
        install_requires=['pygame']

)
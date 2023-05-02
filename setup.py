from setuptools import find_packages, setup

setup(
    name='transcriber',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask', 'flask-uploads', 'flask_wtf', 'WTForms', 'git+https://github.com/openai/whisper.git', 'torch'
    ],
)
import codecs
from setuptools import setup, find_packages

with codecs.open('README.rst',encoding="utf-8") as f:
    readme = f.read()

setup(
    name='openfxy',
    version='0.1.2',
    python_requires='>=3',
    packages=find_packages(),
    install_requires=[
        "numpy==1.19.0",
        "pandas==0.23.4",
        "scikit-learn==0.23.1",
		"keras==2.3.1",
		"keras-applications==1.0.8",
		"keras-preprocessing==1.1.0",
		"tensorflow==2.2.0",
		"tensorflow-estimator==2.2.0",	
		"nltk==3.5",
		"gensim==3.8.1",
		"requests==2.22.0",
		"scipy==1.4.1",
    ],
    url='https://github.com/404notf0und/FXY',
    license='MIT License',
    author='404 Not Found',
    author_email='root@4o4notfound.org',
    description='Security-Scenes-Feature-Engineering-Toolkit, Continuous Integration. ',
    long_description_content_type="text/x-rst",
    long_description=readme,
)
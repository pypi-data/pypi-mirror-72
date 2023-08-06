from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='globus.etl.utils',
    version='0.0.2',
    description='ETL tools for Globus Staffing',
    #package_dir={'': 'src'},
    #long_description_content_type="text/markdown",
    #long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='globus.ai',
    author_email='zhas@globus.ai',
    keywords=['Staffing', 'ETL'],
    url='https://bitbucket.org/dedicare/globus_etl_utils/src/develop/',
    download_url='https://pypi.org/project/globusetlutils/'
)

install_requires = [
    'pytz>=2019.3',
    'pyodbc>=4.0.30',
    'pymongo>=3.8.0',
    'requests>=2.23.0',
    'azure-storage-blob>=0.37.0',
    'pyspark>=3.0.0',
    'python_dateutil>=2.8.1',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
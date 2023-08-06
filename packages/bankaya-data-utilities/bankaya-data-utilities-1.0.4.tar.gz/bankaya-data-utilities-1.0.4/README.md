# Data Utilities

Library for data utilities to connect to MySQL and Dynamo Databases.

## Deploying code to pypi

To deploy the code just add to your home directory the .pypirc file with the following lines:

```
[distutils]
index-servers=pypi

[pypi]
username = __token__
password = <your_pypi_account_token>
```
Then build the binary code with the following command:
```
$ python setup.py sdist
```
Then register and upload the code with the command:
```
$ twine upload dist/* --verbose
```
Note: twine is installed with pip install twine
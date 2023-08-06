Useful ETL tools for Globus Staffing

# Description
    
It consists of 14 modules:

- `job`: create job instance
- `json`: tools to work with json
- `spark`: tools to work with spark
- `spark_job`: tools to work with spark job
- `utils`: tools to connect to db
- `config_reader`: tools to work with config file
- `pipeline`: toolscreate pipeline
- `tenant_service`: create tenant service instance 
- `persistance_service`: create persistance service instance 
- `backend_service`: create backend service instance  
- `backend_candidates_service`: create backend candidate service instance 
- `recman_service`: create recman service instance 
- `tenant_aware_job`: tools to work with tenant job
- `tenant_aware_spark_job`: tools to work with tenant spark job


# Installation
 
## Normal installation

```bash
pip install globus_etl_utils
```

## Development installation

```bash
git clone https://[USER NAME]@bitbucket.org/dedicare/globus_etl_utils.git
cd globus_etl_utils
pip install --editable .
```

# Pip package publishing

```
pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

```
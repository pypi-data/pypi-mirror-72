# The Cloudframe Data Scientist Enabler

At Cloudframe we employ teams of Data Scientists, Data Engineers, and Software Developers.  Check us out at [http://cloudframe.io](http://cloudframe.io "Cloudframe website")

If you're interested in joining our team as a Data Scientist see here: [Bid Prediction Repo](https://github.com/cloudframe/texas-bid-prediction).  There you'll find a fun problem and more info about our evergreen positions for Data Scientists, Data Engineers, and Software Developers.

This package contains some convenience functions meant help a Data Scientist:
* get data into a format that is useful for training models,
* track experiments as a natural workflow, and
* submit training jobs as part of the Command Data Science Environment (CDSE).
  
It is a light version of some of our proprietary enablers that we use to deliver data-informed products to our clients.  The `workflow` sub-module contains `tracker` which is intended to support data science experimentation.

## Installation

`pip install datascientist`

## Dependencies

In addition to the following packages, `datascientist` requires that you have the credentials (et cetera) to perform the operation required.  For example, when connecting to a Redshift database you must have the correct credentials stored either as environment variables (see the example bash profile) or in an `rs_creds.json` file located in the home directory.  

* `pandas`
* `numpy`
* `psycopg2`
* `PyYAML`

## Structure

```
data-scientist/
|
|-- connections/
|   |-- __init__.py
|   |-- rsconnect.py
|
|-- workflow/
|   |-- __init__.py
|   |-- tracker.py
|
|-- Manifest.in
|-- README.md
|-- setup.py
|-- bash_profile_example
```

## Usage

### `connections.rsconnect`

A set of convenience functions for interacting with a Redshift database.  In addition to merely establishing connections and fetching data, this sub-module can perform do things like:

* Infer the schema of your DataFrame
* CREATE and DROP tables
* WRITE data to a table 
* Perform an UPSERT operation
* Get the names of tables in your cluster
* Et cetera

For example, upsert data or write a new table:

```
import connections.rsconnect as rs

tname = 'my_table'

fields = rs.infer_schema(df)
bucket, key = rs.df_to_s3(df, 
                          bucket = 'my-bucket', 
                          key = 'location/on/s3/my-file.csv',
                          primary = 'my_primary_key')

if rs.table_check(tname):
    _ = rs.upsert_table(tname, 
                        fields, 
                        bucket = bucket,
                        key = key,
                        primary = 'my_primary_key')

else:
    _ = rs.create_table(tname, 
                        fields,
                        primary = 'my_primary_key')
    _ = rs.write_data(tname,
                      bucket,
                      key)
```

Note also that the function to fetch data is: `rs.sql_to_df()`.

### `workflow.tracker`

The `workflow.tracker` provides a lightweight tool for tracking a data science workflow.  It is intended to help data scientists produce human-readable artifacts and obviate the need for things like complex naming conventions to keep track of the state of modeling experiments.  It also has features to enable reproducibility, iterative improvment, and model deployent in a cloud environment (AWS right now).

The fundamental object of this library is the `Project` class.  A Project conceptually is a single effort to build a Machine Learning function to address a particular problem.  Individual experiments are conceptualized as 'runs'.  A Run covers the data science workflow from data conditioning (post ETL and feature generation) through model validation and testing.  

For more information and to learn how to use the Workflow Tracker, see the sample notebooks in the ['cloud-event-modeling'](https://github.com/cloudframe/cloud-event-modeling/) repository.  

### `jobs.training`

The `jobs.training` module contains the complement to the Command Data Science Environment by Cloudframe, eanbling no-fuss distributed training.  See xxxx for more info.
# Download SQL assets

- Download at https://drive.google.com/drive/folders/1moeWYoUtUklJO6NJdWo9OV8zWjRn0rjN
- Install `psql` and connect to your choice of Cloud Postgres DB

## Running scripts to build `sql_course` database

- Execute [create_database_sql](./1_create_database.sql)
- Execute [create_tables_sql](./2_create_tables.sql)
- Follow instructions from [3_modify_tables.sql](./3_modify_tables.sql):

```psql
 \copy company_dim FROM '/home/thangtran3112/Downloads/all_folders/csv_files/company_dim.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

 \copy skills_dim FROM '/home/thangtran3112/Downloads/all_folders/csv_files/skills_dim.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

 \copy job_postings_fact FROM '/home/thangtran3112/Downloads/all_folders/csv_files/job_postings_fact.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

 \copy skills_job_dim FROM '/home/thangtran3112/Downloads/all_folders/csv_files/skills_job_dim.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');
```

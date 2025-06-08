import os
import csv
import psycopg2
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from io import StringIO
from psycopg2 import sql

def dbt_branch(keys):
    print("Running DBT script with keys:", keys)
    
    # PostgreSQL Configuration
    db_host = 'host.docker.internal'
    db_port = 5439
    db_name = 'reddit'
    db_user = 'admin'
    db_password = 'AdminPassword123'

    s3_hook = S3Hook(aws_conn_id='awsID')
    bucket_name = 'rabbitmq-reddit'

    # Establish database connection
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )

    for key in keys:
        try:
            # Get S3 object
            obj = s3_hook.get_key(bucket_name=bucket_name, key=key)
            csv_content = obj.get()['Body'].read().decode('utf-8')
            
            # Create file-like object
            csv_file = StringIO(csv_content)
            
            # Extract table name from S3 key
            filename = os.path.basename(key)
            table_name = os.path.splitext(filename)[0]  # Remove file extension
            
            # Read header row
            header = next(csv.reader([next(csv_file)]))
            
            with conn.cursor() as cursor:
                # Drop table if exists
                drop_query = sql.SQL("DROP TABLE IF EXISTS {}").format(
                    sql.Identifier(table_name)
                )
                cursor.execute(drop_query)
                
                # Create new table
                create_query = sql.SQL("CREATE TABLE {} ({})").format(
                    sql.Identifier(table_name),
                    sql.SQL(', ').join(
                        sql.Identifier(col) + sql.SQL(" TEXT") for col in header
                    )
                )
                cursor.execute(create_query)
                
                # Copy data using CSV format
                copy_cmd = sql.SQL("COPY {} FROM STDIN WITH (FORMAT CSV)").format(
                    sql.Identifier(table_name)
                )
                cursor.copy_expert(copy_cmd.as_string(conn), csv_file)
                
            conn.commit()
            print(f"Created table '{table_name}' with {len(header)} columns")

        except Exception as e:
            conn.rollback()
            print(f"Error processing {key}: {str(e)}")
            raise

    conn.close()
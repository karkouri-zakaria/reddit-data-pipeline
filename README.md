![Python](https://img.shields.io/badge/Language-Python%203.10-blue?logo=python&logoColor=white)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC?logo=terraform&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/Messaging-RabbitMQ-FF6600?logo=rabbitmq&logoColor=white)
![Celery](https://img.shields.io/badge/Task%20Queue-Celery-37814A?logo=celery&logoColor=white)
![AWS](https://img.shields.io/badge/Cloud-AWS-232F3E?logo=amazon-aws&logoColor=white)
![Airflow](https://img.shields.io/badge/Orchestrator-Apache%20Airflow-017CEE?logo=apache-airflow&logoColor=white)
![dbt](https://img.shields.io/badge/Transformation-dbt-FD5126?logo=dbt&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-316192?logo=postgresql&logoColor=white)
![TensorFlow](https://img.shields.io/badge/ML-TensorFlow-FF6F00?logo=tensorflow&logoColor=white)
![Superset](https://img.shields.io/badge/BI-Apache%20Superset-orange?logo=apache-superset&logoColor=white)
![LocalStack](https://img.shields.io/badge/Cloud%20Emulation-LocalStack-purple?logo=localstack&logoColor=white)

## 📬 Contact

[![GitHub](https://img.shields.io/badge/GitHub-karkouri--zakaria-181717?logo=github)](https://github.com/karkouri-zakaria)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Karkouri%20Zakaria-blue?logo=linkedin)](https://www.linkedin.com/in/karkouri-zakaria/)
[![Email](https://img.shields.io/badge/Email-zakaria.karkouri%40outlook.com-red?logo=gmail)](mailto:zakaria.karkouri@outlook.com)
[![Facebook](https://img.shields.io/badge/Facebook-Karkouri%20Zakaria-1877F2?logo=facebook&logoColor=white)](https://www.facebook.com/karkouri.zakaria/)
[![Instagram](https://img.shields.io/badge/Instagram-zakaria.karkouri-E4405F?logo=instagram&logoColor=white)](https://www.instagram.com/zakaria.karkouri/)

---

# Reddit Data Processing Pipeline

## Table of Contents
- [Project Overview](#project-overview)
- [Real-World Scenario](#real-world-scenario)
- [Architecture Components](#architecture-components)
- [Pipeline Workflow](#pipeline-workflow)
- [All Containerized](#all-containerized)
- [🐳 Setup](#-setup)
- [🚀 Quickstart](#-quickstart)
- [📁 Project Folder Hierarchy](#-project-folder-hierarchy)
- [📊 Walkthrough](#-walkthrough)
- [📌 Conclusion](#-conclusion)
- [🔭 What's Next](#-whats-next)

# Project Overview
This project implements an end-to-end data pipeline for processing Reddit data using modern DevOps and data engineering tools. The architecture enables automated data collection, message queue processing, cloud storage, workflow orchestration, and visualization - all running in a containerized local environment. The solution demonstrates how to build a production-grade data pipeline using open-source technologies.

# Real-World Scenario
### Social Media Analytics Platform
Imagine a media intelligence company that monitors Reddit for brand sentiment analysis. This pipeline would:
1. Continuously collect posts from target subreddits
2. Process data with NLP for sentiment scoring
3. Track trending topics in real-time
4. Generate executive dashboards with engagement metrics
5. Provide historical analysis of discussion patterns

# Architecture Components

### Core Technologies
1. **RabbitMQ** (v3-management)  
   *Message broker for task queuing*  
   - Manages communication between components

2. **Celery with Pika**  
   *Distributed task queue system*  
   - Processes messages from RabbitMQ
   - Scales worker nodes based on load

3. **LocalStack**  
   *AWS cloud service emulator*  
   - Provides local S3 storage (`rabbiting-reddit` bucket)
   - Emulates Redshift API (using PostgreSQL backend)

4. **PostgreSQL as Redshift Emulator**  
   *Analytical database*  
   - Stores raw and processed data
   - Schemas:
     - `raw`: Ingested data (`reddit_*` tables)
     - `dev`: Processed data (`reddit_posts` table)

5. **Apache Airflow**  
   *Workflow orchestration*  
   - Schedules and monitors data pipelines

6. **Apache Superset**  
   *Data visualization platform*  
   - Creates dashboards from analyzed data

### Supporting Technologies
- **Terraform**: Infrastructure provisioning
- **TensorFlow**: Machine learning components

# Pipeline Workflow
![workflow](images/Presentation.jpg)

# All Containerized

All our services will be containerized using **Docker** to benefit from:

- ✅ **Isolation**: Each service runs in its own container, avoiding dependency conflicts.
- 🔁 **Reproducibility**: Environments are consistent across development, testing, and production.
- ⚙️ **Scalability**: Easy to scale individual services like Celery workers or database instances.
- 🚀 **Portability**: Containers can run anywhere; locally, on servers, or in the cloud.
- ⏱️ **Faster Deployment**: Services start quickly and integrate smoothly with CI/CD pipelines.
- 🔧 **Simplified Setup**: Dependencies and configurations are bundled within the container images.
- 📦 **Modularity**: Easily maintain or swap services like PostgreSQL, Superset, Airflow, etc.

This approach ensures that our **data pipeline** (from ingestion to visualization) remains **robust, portable, and maintainable**, while enabling team collaboration and cloud migration.

<p align="center">
  <img src="images/image-22.png" alt="Docker" width="45%" />
</p>

---
# 🚀 Quickstart

## Clone the repository and organize folders:

```bash
git clone https://github.com/yourusername/reddit-data-pipeline
```

# 📁 Project Folder Hierarchy
### ⚠️ Place each folder into its corresponding Docker container volume
- 🐋 pika_celery_tensorflow/
  - 📁 /app/
    - 📄 consumer.py
    - 📄 main.tf
    - 📄 producer.py
    - 📄 requirements.txt
    - 📄 tasks.py
    - 📁 Sources/
      - 📄 *.xslx

- 🐋 airflow_dbt_tensorflow/
  - 📁 /home/airflow/.dbt/
    - 📄 profiles.yml
  - 📁 /opt/airflow/
    - 📄 requirements.txt
    - 📄 simple_auth_manager_passwords.json.generated
    - 📁 dags/
      - 📄 conditional.py
    - 📁 scripts/
      - 📄 dbt_branch.py
      - 📄 tf_branch.py
      - 📁 reddit/ (created by `dbt init`)
        - 📁 modals/
          - 📄 reddit_posts.sql
          - 📄 sources.yml
        - 📁 macros/
          - 📄 list_raw_tables.sql
---

## Source of our data

[Reddit WallStreetBets Posts Sentiment Analysis (Kaggle)](https://www.kaggle.com/code/thomaskonstantin/reddit-wallstreetbets-posts-sentiment-analysis?select=reddit_wsb.csv)

<p align="center">
  <img src="images/image-28.png" alt="Kaggle" width="45%" />
</p>

# 🐳 Setup

- RabbitMQ
- Localstack
- Airflow
- PostgreSQL
- Apache Superset
- Pika_celery_terraform
- Terraform
 Run:
```bash
docker compose up -d
```

You'll still need to run these commands after the container starts:
```bash
docker exec -it superset bash -c "pip install psycopg2-binary"
docker exec -it superset superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@example.com \
  --password admin
docker exec -it superset superset db upgrade
docker exec -it superset superset init
docker exec -it airflow_dbt_tensorflow export AIRFLOW_CONN_AWSID='aws://test:test@?region_name=us-east-1&endpoint_url=http://host.docker.internal:4566'
```

## Access Details

| Service       | URL                                  | Credentials            |
|---------------|--------------------------------------|------------------------|
| RabbitMQ      | http://localhost:15672               | guest/guest            |
| LocalStack    | https://localhost.localstack.cloud:4566 | N/A                    |
| Airflow       | http://localhost:8080                | From project files     |
| Superset      | http://localhost:8011                | admin/admin            |
| PostgreSQL    | localhost:5439                       | admin/AdminPassword123 |

**Notes:**
- PostgreSQL uses port 5439 to avoid conflicts with default PostgreSQL installations
- Airflow credentials are stored in the project directory

⚠️ **To mention:**
Although we can simulate Redshift using the following LocalStack command:
```bash
docker exec localstack awslocal redshift create-cluster --cluster-identifier reddit-cluster --db-name reddit --master-username admin --master-user-password AdminPassword123 --node-type dc2.large --cluster-type single-node --publicly-accessible
```
This is only an **API simulation** not for development. Since Redshift is built on top of **PostgreSQL**, we use a PostgreSQL container as a practical emulator for local development and testing.

# 📊 Walkthrough

### 1. Inspecting the RabbitMQ Queue

We begin by accessing the **RabbitMQ interface** to inspect the queue named `"task_queue"`, which is where our application is expected to receive and store messages fetched from the Reddit API.

![RabbitMQ Queue View](images/image.png)  
![Queue Detail View](images/image-1.png)

---

### 2. Terraform: S3 Bucket and IAM Creation

After executing the Terraform script, it automatically provisions an **S3 bucket** and the associated **IAM role/policy**. These resources are configured to store messages received from RabbitMQ in CSV format.

![S3 Bucket Created via Terraform](images/image-2.png)

---

### 3. Starting the Celery Worker

We launch the **Celery worker** responsible for consuming messages from the `"task_queue"` by running the following command:

```bash
celery -A tasks worker --loglevel=info --queues=task_queue
```
![alt text](images/image-3.png)

### 4. Emulating the Reddit API with Pika Producer

Since access to the actual **Reddit API** is unavailable, we emulate its behavior using a **RabbitMQ producer** implemented with **Pika** in the `producer.py` script and the excel file `Sources/reddit_20231023.xlsx`. This allows us to simulate data being sent to our queue as if it came from the Reddit API.

⚙️ **Key Difference between Celery and Pika**:
- **Pika** is a low-level RabbitMQ client that streams raw data without any abstraction or task management features.
- **Celery**, on the other hand, offers advanced capabilities such as task retries, scheduling, and result tracking, making it ideal for production-ready distributed task queues.

![Simulated Producer Using Pika](images/image-4.png)


### 5. Verifying S3 Bucket Creation in LocalStack

After executing the Terraform script, we verify the successful creation of our **S3 infrastructure** via the **LocalStack Cloud dashboard**.

By navigating to [LocalStack Dashboard](https://app.localstack.cloud/dashboard), we confirm that:
- The **S3 service** is active.
- Our **bucket** has been created.
- The **CSV file**, generated from the received Reddit messages, is stored correctly in the bucket.

This confirms that the pipeline is functioning as intended.

![S3 Bucket Created](images/image-5.png)
![CSV File in Bucket](images/image-6.png)


## Orchestration with Airflow: Conditional S3 Branching DAG

We move on to orchestrating our workflow using **Apache Airflow**.

### DAG: `conditional_s3_branching`

This DAG is designed to **monitor updates in our S3 files** and execute different tasks based on the presence or absence of those files.

#### Workflow structure:

- **start**  
  The entry point of the DAG, initiating the process.

- **check_files**  
  This task checks the S3 bucket for updated or new files. It acts as a conditional gate to determine which path the workflow should follow next.

- From **check_files**, the workflow branches into three possible paths:  
  - **run_dbt_task** ;  triggers dbt (data build tool) operations, such as data transformation and testing.  
  - **run_tensorflow_task** ;  starts TensorFlow-related tasks for any machine learning processing needed on the data and then into a **join** step.  
  - **no_files_found** ;  runs when no relevant files are found in S3, effectively a fallback or end state to avoid running unnecessary processes.

- **run_dbt_task** flows into:  
  - **dbt_run_and_test** (for dbt tasks) and then into a **join** step that synchronizes the parallel branches.

- The **no_files_found** task also flows into the same **join** task, ensuring all paths converge properly to complete the DAG run.

---

This conditional branching allows efficient resource usage by only running computationally expensive tasks when new data is available.

![DAG Overview](images/image-7.png)
![Check Files Task](images/image-8.png)
![Branching Structure](images/image-9.png)


## TensorFlow Training Script

The TensorFlow script performs the following:

- **Loads the training data directly from the CSV file stored in the S3 bucket.**
- **Trains a machine learning model using this data.**
- **Displays summary information about the training dataset and the model’s training process,** such as loss, accuracy, or other relevant metrics.
- **The model is trained in this case on the reltionship number of comments / score**
- **Saves the trained model locally** for later use, such as inference or further evaluation.
- ### **Our model simple linear regression model**

This approach streamlines the workflow by integrating data loading, model training, and model persistence into a single step within the orchestration pipeline.

![Training Process Overview](images/image-10.png)
![Training Process Overview](images/image-25.png)


## DBT Tasks Overview

### First DBT Task: Load Raw Data

- **Loads the CSV file directly into the PostgreSQL database** as a raw data table.
- The table is created in a schema called `raw`.
- This represents the primitive, unprocessed form of the data ready for further transformation.

![Load Raw Data](images/image-11.png)
![Load Raw Data](images/image-26.png)

### Second DBT Task: Transform and Test Data

- **Runs the DBT models, tests, and macros** to process the raw data.
- Performs tasks such as **column type association, null value cleaning, and other data transformations**.
- The processed and cleaned results are saved in a new table inside the `dev` schema.
- Both `raw` and `dev` DBT schemas are created automatically by DBT during this process.

![Transform and Test Data](images/image-12.png)
![Load Raw Data](images/image-27.png)


## Verifying PosgreSQL Tables and Transformations with psql

- We use the PostgreSQL client `psql` to inspect the database.
- This allows us to check if the tables have been created with the expected schemas.
- We also verify that the desired data transformations have been applied correctly.

![Check Tables](images/image-13.png)  
![Verify Transformations](images/image-14.png)


## Superset Visualization

Last but not least, we start **Apache Superset** for data exploration and dashboarding.

- We connect Superset to our PostgreSQL database.
- From there, we create a **dataset** based on the `dev.reddit_posts` table.
- Once the dataset is loaded, we begin creating visualizations.

📊 In our example, we build a chart showing the **count of scores** based on the **number of comments**.

This allows us to:
- Explore how engagement (comments) affects scoring.
- Visually verify the effectiveness of our ETL pipeline.

### The connection string is:
```bash
postgresql://admin:AdminPassword123@host.docker.internal:5439/reddit
```

![Superset Home](images/image-15.png)  
![Database Connection](images/image-16.png)
![Dataset View](images/image-17.png)  
![Chart Creation](images/image-18.png)  
![Chart Settings](images/image-19.png)  
![Final Visualization](images/image-20.png)

# 📌 Conclusion

This project illustrates a hands-on integration of distributed systems, orchestration, and data transformation workflows within a modular, containerized architecture. By simulating real-world cloud services and data flows, we’ve created a reliable environment for experimentation and development without depending on external APIs or infrastructures.

The design promotes autonomy, flexibility, and clarity across each pipeline stage; from ingestion and storage to processing, analysis, and visualization. Every component is loosely coupled yet part of a cohesive system, ensuring maintainability and scalability.

---

# **🔭 What's Next**

- Add automated testing and monitoring; potentially using **Grafana** and **Prometheus**; to ensure performance, reliability, and observability in real time.
- Implement more **dbt tests** and adopt a **Data Quality Framework** to validate schema integrity and track anomalies.
- Introduce **security enhancements** to safeguard sensitive data and manage user access effectively.
- Integrate **advanced analytics** for deeper insights, including trend analysis and predictive modeling.

<p align="center">
  <img src="images/image-23.png" alt="Superset chart showing score distribution by comment count" width="15%" />
  <img src="images/image-24.png" alt="Superset dataset and dashboard setup" width="15%" />
</p>

# License
This project is licensed under the [MIT License](LICENSE).

---

## **Author:** [Karkouri Zakaria](https://github.com/karkouri-zakaria)
import pandas as pd
import pandas_gbq
from google.cloud import bigquery


def run_transfer():

    df_notebook_usage = pandas_gbq.read_gbq('SELECT * FROM `knada-gcp.knorten.stderr_202*`', project_id="nada-prod-6977")
    df_users = pandas_gbq.read_gbq('SELECT * FROM `knada-gcp.knorten.metrics_raw`', project_id="nada-prod-6977")

    table_dict = {"notebook_usage": df_notebook_usage,
                  "knorten_users": df_users}

    client = bigquery.Client(project="nada-prod-6977")


    project, dataset = "nada-prod-6977", "knorten_usage"
    for table in table_dict:
        table_id = f"{project}.{dataset}.{table}"

        job_config = bigquery.job.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

        job = client.load_table_from_dataframe(table_dict[table], table_id, job_config=job_config)



if __name__ == "__main__":
    run_transfer()

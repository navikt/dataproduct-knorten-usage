import pandas as pd
from google.cloud import bigquery


def run_transfer():

    df_notebook_usage = pd.read_gbq('SELECT * FROM `knada-gcp.knorten.stderr_202*`')
    df_users = pd.read_gbq('SELECT * FROM `knada-gcp.knorten.metrics_raw`')

    table_dict = {"notebook_usage": df_notebook_usage,
                  "knorten_users": df_users}

    client = bigquery.Client()
   

    project, dataset = "nada-prod-6977", "knorten_usage"
    for table in table_dict:
        table_id = f"{project}.{dataset}.{table}"

        job_config = bigquery.job.LoadJobConfig(write_disposition="WRITE_TRUNCATE")

        job = client.load_table_from_dataframe(table_dict[table], table_id, job_config=job_config)



if __name__ == "__main__":
    run_transfer()

from ovotestkit.func import AirflowClient

def test_get_variable():
    airflow = AirflowClient()

    vars = airflow.get_variable('job_id_ovo_spring_gold')
    print(vars)

if __name__ == "__main__":
    test_get_variable()
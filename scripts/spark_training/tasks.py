from invoke import task
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType

TOPIC = "topic"
BOOTSTRAP_SERVER = "host.docker.internal:9092"

@task
def start_structured_stream(_):


    spark = SparkSession.builder.master("spark://172.20.0.10:7077") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1") \
        .appName("Stream Processer").getOrCreate()


    df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", BOOTSTRAP_SERVER) \
        .option("subscribe", TOPIC).load()

    query = df.select(col("key").cast(StringType()).alias("key"), col("value").cast(StringType()).alias("value"), col("partition")) \
        .writeStream \
        .format("console") \
        .option("checkpointLocation", "checkpoint/") \
        .start()

    query.awaitTermination()

@task
def apache_airflow_spark(_):
    from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
    from airflow.models import DAG
    from datetime import datetime

    DAG_ID = "foo"
    spark_master = "spark://172.20.0.10:7077"

    with DAG(
        dag_id=DAG_ID,
        schedule=None,
        start_date=datetime(2021, 1, 1),
        catchup=False,
        tags=["example"],
    ) as dag:

        spark_job_1 = SparkSubmitOperator(
            task_id="spark_job1",
            application="/usr/local/spark/app/hello-world.py", # Spark application path created in airflow and spark cluster
            name="foo1",
            conn_id="spark_default",
            verbose=1,
            conf={"spark.master":spark_master},
            dag=dag
        )

        spark_job_2 = SparkSubmitOperator(
            task_id="spark_job2",
            application="/usr/local/spark/app/hello-world.py", # Spark application path created in airflow and spark cluster
            name="foo2",
            conn_id="spark_default",
            verbose=1,
            conf={"spark.master":spark_master},
            dag=dag
        )

        spark_job_1 >> spark_job_2

@task
def apache_airflow(_):

    from datetime import datetime, timedelta
    from textwrap import dedent

    # The DAG object; we'll need this to instantiate a DAG
    from airflow import DAG

    # Operators; we need this to operate!
    from airflow.operators.bash import BashOperator
    with DAG(
        "tutorial",
        # These args will get passed on to each operator
        # You can override them on a per-task basis during operator initialization
        default_args={
            "depends_on_past": False,
            "email": ["airflow@example.com"],
            "email_on_failure": False,
            "email_on_retry": False,
            "retries": 1,
            "retry_delay": timedelta(minutes=5),
            # 'queue': 'bash_queue',
            # 'pool': 'backfill',
            # 'priority_weight': 10,
            # 'end_date': datetime(2016, 1, 1),
            # 'wait_for_downstream': False,
            # 'sla': timedelta(hours=2),
            # 'execution_timeout': timedelta(seconds=300),
            # 'on_failure_callback': some_function,
            # 'on_success_callback': some_other_function,
            # 'on_retry_callback': another_function,
            # 'sla_miss_callback': yet_another_function,
            # 'trigger_rule': 'all_success'
        },
        description="A simple tutorial DAG",
        schedule=timedelta(days=1),
        start_date=datetime(2023, 1, 27),
        catchup=False,
        tags=["example"],
    ) as dag:

        # t1, t2 and t3 are examples of tasks created by instantiating operators
        t1 = BashOperator(
            task_id="print_date",
            bash_command="date",
        )

        t2 = BashOperator(
            task_id="sleep",
            depends_on_past=False,
            bash_command="sleep 5",
            retries=3,
        )
        t1.doc_md = dedent(
            """\
        #### Task Documentation
        You can document your task using the attributes `doc_md` (markdown),
        `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
        rendered in the UI's Task Instance Details page.
        ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
        **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
        """
        )

        dag.doc_md = __doc__  # providing that you have a docstring at the beginning of the DAG; OR
        dag.doc_md = """
        This is a documentation placed anywhere
        """  # otherwise, type it like this
        templated_command = dedent(
            """
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7)}}"
        {% endfor %}
        """
        )

        t3 = BashOperator(
            task_id="templated",
            depends_on_past=False,
            bash_command=templated_command,
        )

        t1 << [t2, t3]
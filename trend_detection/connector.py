import presto
import psycopg2


def getConnection(db_type: str):

    if db_type == 'postgres':
        conn = psycopg2.connect(
            "dbname='d1qak40as4pdj' user='yijzzqjzepuqwk' host='ec2-34-252-251-16.eu-west-1.compute.amazonaws.com' password='6c6b12d9297a9da1d534c47a3a4d1b498377ec12e17a2360cadd247c2f4f7c5d'")
    elif db_type == 'presto':
        conn = presto.dbapi.connect(
            host='-',
            port=443,
            user='-',
            auth=presto.auth.BasicAuthentication("-", "-"),
            catalog='-',
            http_scheme='https',
            schema='-',
        )

    cur = conn.cursor()

    return cur


def getConnectionPostgres():

    cur = conn.cursor()

    return cur

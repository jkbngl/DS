import presto
import psycopg2


def getConnection(db_type: str):

    if db_type == 'postgres':
        conn = psycopg2.connect(
            "dbname='postgres' user='postgres' host='35.198.97.21' password='dhjihdfjdksfhdfhsdfj'")
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

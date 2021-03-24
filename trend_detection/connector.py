import presto

def getConnection():

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

import psycopg2

def load_data(db_connect, data_sets):

    conn = psycopg2.connect(host=db_connect['HOST'],
                            dbname=db_connect['DATABASE'],
                            user=db_connect['USER'],
                            password=db_connect['PASSWORD'])
    cur = conn.cursor()

    insert = """
             insert into sales values(%s, %s, %s, %s, %s, %s);
             """
    
    for data_set in data_sets:
        with open(data_set) as f:
            for line in f:
                values = line.strip().split(',')
                cur.execute(insert, values)

    conn.commit()
    cur.close()
    conn.close()
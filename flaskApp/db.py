import MySQLdb
from flask import current_app


def connection():
    conn = MySQLdb.connect(host= current_app.config['HOST'],
                           user= current_app.config['USER'],
                           passwd= current_app.config['PASSWORD'],
                           db=current_app.config['DATABASE'],)
    c = conn.cursor()

    return c, conn


import MySQLdb

host = '127.0.0.1'
user = 'valtx_dev'
password = 'valtx'
port = 3306
db = 'valtx_test'

conn = MySQLdb.connect(
    host=host,
    user=user,
    passwd=password,
    port=port,
    db=db
)
cursor = conn.cursor()


def get_asset_state(asset_name):
    cursor.execute("""select Estado from mytable where Nombre_del_Activo = '{0}' order by Ultimo_Escaneo DESC""".format(asset_name.upper()))
    return cursor.fetchone()[0]


def get_person_assets(name, last_name):
    cursor.execute("""select Nombre_del_Activo, Username from mytable where Persona_Asignada like '{0}%{1}%'""".format(name.upper(), last_name.upper()))
    return ", ".join(["{0} | {1}".format(row[0], row[1]) for row in cursor.fetchall()])


def get_inactive_n_days(num_days):
    cursor.execute(""" select Nombre_del_Activo from mytable where Estado = 'INACTIVO' and Ultimo_Escaneo < now() - interval {0} day group by Nombre_del_Activo""".format(num_days))
    return ", ".join([row[0] for row in cursor.fetchall()])


def get_users_multiple_assets():
    cursor.execute(""" select Persona_Asignada from mytable group by Persona_Asignada having count(Persona_Asignada) > 1 """)
    return ", ".join([row[0] for row in cursor.fetchall()])


def get_asset_info(asset_name):
    cursor.execute("""select Username, Persona_Asignada, Estado from mytable where Nombre_del_Activo = '{0}'""".format(asset_name.upper()))
    return ", ".join(["{0}".format(" | ".join(row)) for row in cursor.fetchall()])


def get_asset_info_complete(asset_name):
    cursor.execute("""select Username, Direccion_IP, Persona_Asignada, Gerencia, Estado, Sede from mytable where Nombre_del_Activo = '{0}'""".format(asset_name.upper()))
    return ", ".join(["{0}".format(" | ".join(row)) for row in cursor.fetchall()])

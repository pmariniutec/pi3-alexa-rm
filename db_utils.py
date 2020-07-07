import MySQLdb

host = '127.0.0.1'
user = 'valtx_dev'
password = 'valtx'
port = 3306
db = 'otrs'

conn = MySQLdb.connect(
    host=host,
    user=user,
    passwd=password,
    port=port,
    db=db
)
cursor = conn.cursor()


def get_asset_state(asset_name):
    cursor.execute("""select estado_equipo from cmdb_cpu where name = '{0}'""".format(asset_name.upper()))
    try:
        return cursor.fetchone()[0]
    except:
        return None


def get_person_assets(name, last_name):
    cursor.execute("""select cpu.name, cu.email from customer_user cu
                      join cmdb_cpu cpu 
                      on cpu.owner = cu.customer_id
                      where cu.first_name = '{0}' and cu.last_name  = '{1}'""".format(name.upper(), last_name.upper()))
    try:
        return list(cursor.fetchall())
    except:
        return None


def get_inactive_n_days(num_days):
    cursor.execute("""select cpu.name from cmdb_cpu cpu
                      where cpu.estado_equipo = 'Inoperativo' and cpu.fecha_mod  < now() - interval {0} day""".format(num_days))
    try:
        return len([row[0] for row in cursor.fetchall()])
    except:
        return None


def get_users_multiple_assets():
    cursor.execute(""" select cu.first_name, cu.last_name from cmdb_cpu cpu
                       join customer_user cu
                       on cu.customer_id = cpu.owner
                       group by cu.customer_id having count(cu.customer_id) > 1 """)
    try:
        return ", ".join(["{0} {1}".format(row[0], row[1]) for row in cursor.fetchall()])
    except:
        return None


def get_asset_assignee(asset_name):
    cursor.execute("""select cu.first_name, cu.last_name from cmdb_cpu cpu
                      join customer_user cu
                      on cu.customer_id = cpu.owner
                      where cpu.name  = '{0}'""".format(asset_name.upper()))
    try:
        return "".join(["{0} {1}".format(row[0], row[1]) for row in cursor.fetchall()])
    except:
        return None


def get_asset_info_complete(asset_name):
    cursor.execute("""select cu.customer_id, cu.first_name, cu.last_name, cpu.estado_equipo, cpu.deployment_state, cpu.tipo_propiedad, cpu.ubicacion
                      from cmdb_cpu cpu
                      join customer_user cu
                      on cu.customer_id = cpu.owner
                      where cpu.name  = '{0}'""".format(asset_name.upper()))
    return ", ".join(["{0}".format(" | ".join(row)) for row in cursor.fetchall()])

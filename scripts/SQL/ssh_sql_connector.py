import src.pysql.pySQL as sqlconn
import conn as conn


def SQL_connector():
    ssh = sqlconn.SSHtunnel(
        ssh_host=conn.ssh_host,
        ssh_username=conn.ssh_username,
        ssh_password=conn.ssh_password,
        remote_bind_address=conn.remote_bind_address,
    )
    tunnel = ssh.create_tunnel()
    tunnel.start()
    sql = sqlconn.SQL(
        host=conn.host,
        database=conn.database,
        user=conn.user,
        password=conn.password,
        port=tunnel.local_bind_port,
        connect_type="MySQL",
    )

    return sql

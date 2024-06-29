import mariadb 
from getpass import getpass

def main():
    print("""For this script, a root level account on a mariadb instance is required. I programmed this to use a command-line interface to
        make it possible to run through an SSH terminal. \n""")
    e_hn = input("Enter hostname of the server: [default = localhost] ")
    if e_hn == "":
        e_hn = "localhost"
    e_port = input("Enter the port of the server: [default = 3306] ")
    if e_port == "":
        e_port = 3306
    else:
        try:
            e_port = int(e_port)
        except:
            print("Port has to be an integer (whole number) value. Please run script again and use the default if you're unsure.")
    e_user = input("Enter the username of the root-level account: [default = root] ")
    if e_user == "":
        e_user = "root"
    e_passwd = getpass("Enter the root-level user's password: [default = blank] ")

    perm_check = 0
    try:
        conn = mariadb.connect(host=e_hn, port=e_port, user=e_user, password=e_passwd)
        cur = conn.cursor()
        cur.execute("SHOW GRANTS")
        results = cur.fetchall()
        for r in results:
            r = r[0]
            if r.startswith(f"GRANT ALL PRIVILEGES ON *.* TO `{e_user}`"):
                perm_check += 1
            if r.endswith(f"WITH GRANT OPTION"):
                perm_check += 1
    except:
        print("Was not able to login to the server. Please check credentials and try again.")
    if perm_check < 2:
        print("Permissions are not sufficient. Please try again with a root-level user.")
        quit()
    else:
        print("Permissions good, continuing.")

    e_ndb = input("Enter the name of the database you want to create: [default = tam] ")
    if e_ndb == "":
        e_ndb = "tam"
    cur.execute(f"CREATE DATABASE `{e_ndb}` DEFAULT CHARACTER SET 'utf8mb4' DEFAULT COLLATE 'utf8mb4_bin'")
    cur.execute(f"USE `{e_ndb}`")
    cur.execute("CREATE TABLE prefixes (prefix VARCHAR(150) NOT NULL PRIMARY KEY, bootstyle VARCHAR(150) NOT NULL)")
    conn.commit()

    e_auser = input(f"Enter the username of the admin user you want to create: [default = {e_ndb}_admin] ")
    if e_auser == "":
        e_auser = f"{e_ndb}_admin"
    e_apasswd = getpass("Enter the password for the new admin user: [default = blank] ")
    cur.execute(f"CREATE USER '{e_auser}'@'%' IDENTIFIED BY '{e_apasswd}'")
    cur.execute(f"GRANT ALL PRIVILEGES ON `{e_ndb}`.* TO '{e_auser}'@'%' WITH GRANT OPTION")
    conn.commit()

    e_uuser = input(f"Enter the username of the user-level user you want to create: [default = {e_ndb}_user] ")
    if e_uuser == "":
        e_uuser = f"{e_ndb}_user"
    e_upasswd = getpass("Enter the password for the new user-level user: [default = blank] ")
    cur.execute(f"CREATE USER '{e_uuser}'@'%' IDENTIFIED BY '{e_upasswd}'")
    cur.execute(f"GRANT SELECT, INSERT, UPDATE ON `{e_ndb}`.* TO '{e_uuser}'@'%'")
    cur.execute("FLUSH PRIVILEGES")
    conn.commit()

    host_name = socket.gethostname()
    ipaddr = socket.gethostbyname(host_name)

    print(f"""This command completed successfully. You should be able to point to this server in the client while using your 
    credentials specified in this run of the script. \nIf you ran this script on a separate host server, you have to specify the IP in the client config screen.
    If you're using Linux on the server, running \"ip addr\" in a console and looking for inet can help. On Windows, \"ipconfig\" in a terminal window shows IP addresses.
    Port 3306 or the custom port {e_port} you specified has to be open on the server's firewall.""")

if __name__ == "__main__":
    main()
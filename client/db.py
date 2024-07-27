import mariadb
import ssl
import ttkbootstrap as ttk 
from configparser import ConfigParser

def session_writer():
    window = ttk.Toplevel(title="Write DB Configuration")

    # Variables
    v_explainer = ttk.StringVar(window)
    v_host, v_port = ttk.StringVar(window), ttk.IntVar(window)
    v_user, v_pwd = ttk.StringVar(window), ttk.StringVar(window)
    v_db, v_ssl = ttk.StringVar(window), ttk.BooleanVar(window)

    # Commands
    def cmd_save():
        try:
            config = ConfigParser()
            config["db"] = {
                "host": v_host.get(),
                "port": v_port.get(),
                "user": v_user.get(),
                "password": v_pwd.get(),
                "database": v_db.get(),
                "ssl": v_ssl.get()
            }
            with open("config.ini", "w") as f:
                config.write(f)
            window.destroy()
        except:
            print("Unable to save db file.")
    
    def cmd_read():
        try:
            config = ConfigParser()
            config.read("config.ini")
            dbconfig = config["db"]
            v_host.set(dbconfig["host"])
            v_port.set(dbconfig["port"])
            v_user.set(dbconfig["user"])
            v_pwd.set(dbconfig["password"])
            v_db.set(dbconfig["database"])
            v_ssl.set(dbconfig["ssl"])

            conn, cur = session_maker()
            cur.execute("SHOW TABLES")

            v_explainer.set("Config good, no need to change.")
            lbl_explainer.configure(bootstyle="success")
        except:
            v_port.set(3306)
            v_explainer.set("Config is not good, please check settings below.")
            lbl_explainer.configure(bootstyle="danger")

    def cmd_close():
        window.destroy()

    # Frames
    lbl_explainer = ttk.Label(window, textvariable=v_explainer)
    lbl_explainer.pack(padx=4, pady=4)

    frm_credentials = ttk.Frame(window)
    frm_credentials.pack(padx=4, pady=4)

    frm_buttons = ttk.Frame(window)
    frm_buttons.pack(padx=4, pady=4)

    # Credential controls
    lbl_host = ttk.Label(frm_credentials, text="Hostname/IP")
    lbl_host.grid(row=0, column=0, padx=4, pady=4)

    txt_host = ttk.Entry(frm_credentials, textvariable=v_host, width=15)
    txt_host.grid(row=0, column=1, padx=4, pady=4)

    lbl_port = ttk.Label(frm_credentials, text="Port")
    lbl_port.grid(row=1, column=0, padx=4, pady=4)

    txt_port = ttk.Entry(frm_credentials, textvariable=v_port)
    txt_port.grid(row=1, column=1, padx=4, pady=4)

    lbl_user = ttk.Label(frm_credentials, text="Username")
    lbl_user.grid(row=2, column=0, padx=4, pady=4)

    txt_user = ttk.Entry(frm_credentials, textvariable=v_user)
    txt_user.grid(row=2, column=1, padx=4, pady=4)

    lbl_password = ttk.Label(frm_credentials, text="Password")
    lbl_password.grid(row=3, column=0, padx=4, pady=4)

    txt_password = ttk.Entry(frm_credentials, textvariable=v_pwd, show="*")
    txt_password.grid(row=3, column=1, padx=4, pady=4)

    lbl_db = ttk.Label(frm_credentials, text="Database")
    lbl_db.grid(row=4, column=0, padx=4, pady=4)

    txt_db = ttk.Entry(frm_credentials, textvariable=v_db)
    txt_db.grid(row=4, column=1, padx=4, pady=4)

    lbl_ssl = ttk.Label(frm_credentials, text="SSL")
    lbl_ssl.grid(row=5, column=0, padx=4, pady=4)

    chk_ssl = ttk.Checkbutton(frm_credentials, variable=v_ssl)
    chk_ssl.grid(row=5, column=1, padx=4, pady=4)

    # Button controls
    btn_save = ttk.Button(frm_buttons, text="Save", command=cmd_save)
    btn_save.grid(row=0, column=0, padx=4, pady=4)

    btn_cancel = ttk.Button(frm_buttons, text="Cancel", bootstyle="secondary", command=cmd_close)
    btn_cancel.grid(row=0, column=1, padx=4, pady=4)

    cmd_read()

def session_maker():
    config = ConfigParser()
    try:
        config.read("config.ini")
        config_db = config["db"]
        conndict = {
            "host": config_db["host"],
            "port": int(config_db["port"]),
            "user": config_db["user"],
            "password": config_db["password"],
            "database": config_db["database"],
            "ssl": config_db["ssl"]
        }
        try:
            conn = mariadb.connect(**conndict)
            cur = conn.cursor()
            return conn, cur
        except Exception as e:
            print(e)
            return "error", "No valid db conn"
    except Exception as e:
        print(e)
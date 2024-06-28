from .db import session_maker

class TicketTable():
    def __init__(self, prefix:str):
        self.tablename = f"{prefix}_tickets"
    def create(self):
        conn, cur = session_maker()
        sql_str = f"""CREATE TABLE IF NOT EXISTS `{self.tablename}` (
        ticket_id INT PRIMARY KEY,
        first_name VARCHAR(200),
        last_name VARCHAR(200),
        phone_number VARCHAR(200),
        preference VARCHAR(150) DEFAULT "CALL"
        )"""
        cur.execute(sql_str)
        conn.commit()
        conn.close()
    def insert(self, ticket_id:int, first_name:str, last_name:str, phone_number:str, preference:str):
        conn, cur = session_maker()
        rd = (first_name, last_name, phone_number, preference)
        try:
            sql_str = f"""INSERT INTO `{self.tablename}` (ticket_id, first_name, last_name, phone_number, preference) 
            VALUES ({ticket_id}, \"{first_name}\", \"{last_name}\", \"{phone_number}\", \"{preference}\")"""
            cur.execute(sql_str)
            conn.commit()
        except:
            sql_str = f"""UPDATE `{self.tablename}`
            SET first_name = \"{first_name}\", last_name = \"{last_name}\", phone_number = \"{phone_number}\", preference = \"{preference}\"
            WHERE ticket_id={ticket_id}"""
            cur.execute(sql_str)
            conn.commit()
        print(f"Inserted/Updated record on {ticket_id}")
        conn.close()
    def select(self, ticket_id:int):
        conn, cur = session_maker()
        try:
            cur.execute(f"SELECT * FROM {self.tablename} WHERE ticket_id={ticket_id}")
            result = cur.fetchone()
            conn.close()
            return result
        except:
            return "No record found"
    def select_range(self, start_num:int, end_num:int):
        conn, cur = session_maker()
        result_set = {}
        for i in range(start_num, end_num+1):
            result_set[i] = ["", "", "", "CALL"]
        sql_str = f"""SELECT * FROM `{self.tablename}` WHERE ticket_id BETWEEN {start_num} AND {end_num}"""
        cur.execute(sql_str)
        for r in cur.fetchall():
            result_set[r[0]] = [r[1], r[2], r[3], r[4]]
        conn.close()
        return result_set
    def select_all(self):
        conn, cur = session_maker()
        result_set = {}
        sql_str = f"SELECT * FROM `{self.tablename}`"
        cur.execute(sql_str)
        for r in cur.fetchall():
            result_set[r[0]] = [r[1], r[2], r[3], r[4]]
        conn.close()
        return result_set
    def select_random(self):
        conn, cur = session_maker()
        sql_str = f"SELECT ticket_id FROM `{self.tablename}` ORDER BY RAND() LIMIT 1"
        cur.execute(sql_str)
        result = cur.fetchone()
        conn.close()
        return result[0]
    def drop(self):
        conn, cur = session_maker()
        drop_str = f"DROP TABLE `{self.tablename}`"
        cur.execute(drop_str)
        conn.commit()
        conn.close()

class BasketTable():
    def __init__(self, prefix:str):
        self.tablename = f"{prefix}_baskets"
    def create(self):
        conn, cur = session_maker()
        sql_str = f"""CREATE TABLE IF NOT EXISTS `{self.tablename}` (
        basket_id INT PRIMARY KEY,
        basket_desc VARCHAR(255),
        basket_donor VARCHAR(255),
        winning_ticket INT DEFAULT 0
        )"""
        cur.execute(sql_str)
        conn.commit()
        conn.close()
    def insert(self, basket_id:int, basket_desc:str, basket_donor:str):
        conn, cur = session_maker()
        try:
            sql_str = f"""INSERT INTO `{self.tablename}` (basket_id, basket_desc, basket_donor) 
            VALUES ({basket_id}, \"{basket_desc}\", \"{basket_donor}\")"""
            cur.execute(sql_str)
            conn.commit()
        except:
            sql_str = f"""UPDATE `{self.tablename}`
            SET basket_desc = \"{basket_desc}\", basket_donor = \"{basket_donor}\"
            WHERE basket_id={basket_id}"""
            cur.execute(sql_str)
            conn.commit()
        conn.close()
    def insert_winner(self, basket_id:int, winning_ticket:int):
        conn, cur = session_maker()
        try:
            sql_str = f"""INSERT INTO `{self.tablename}` (basket_id, winning_ticket)
            VALUES ({basket_id}, {winning_ticket})"""
            cur.execute(sql_str)
            conn.commit()
        except:
            sql_str = f"""UPDATE `{self.tablename}`
            SET winning_ticket = {winning_ticket}
            WHERE basket_id={basket_id}"""
            cur.execute(sql_str)
            conn.commit()
        conn.close()
    def select(self, basket_id:int):
        conn, cur = session_maker()
        result_set = {}
        try:
            cur.execute(f"SELECT * FROM {self.tablename} WHERE basket_id={basket_id}")
            result = cur.fetchone()
            result_set[ticket_id] = [result[1], result[2], result[3]]
            conn.close()
            return result_set
        except:
            conn.close()
            return "No record found"
    def select_range(self, start_num:int, end_num:int):
        conn, cur = session_maker()
        result_set = {}
        for i in range(start_num, end_num+1):
            result_set[i] = ["", "", 0]
        sql_str = f"""SELECT * FROM `{self.tablename}` WHERE basket_id BETWEEN {start_num} AND {end_num}"""
        cur.execute(sql_str)
        for r in cur.fetchall():
            result_set[r[0]] = [r[1], r[2], r[3]]
        conn.close()
        return result_set
    def select_all(self):
        conn, cur = session_maker()
        result_set = {}
        sql_str = f"SELECT * FROM `{self.tablename}`"
        cur.execute(sql_str)
        for r in cur.fetchall():
            result_set[r[0]] = [r[1], r[2], r[3]]
        conn.close()
        return result_set
    def drop(self):
        conn, cur = session_maker()
        drop_str = f"DROP TABLE `{self.tablename}`"
        cur.execute(drop_str)
        conn.commit()
        conn.close()

class ReportByName():
    def __init__(self, prefix:str):
        self.reportname = f"{prefix}_r_lastname"
        self.ticket_table = f"{prefix}_tickets"
        self.basket_table = f"{prefix}_baskets"
    def create(self):
        conn, cur = session_maker()
        create_str = f"""CREATE VIEW `{self.reportname}` AS
        SELECT CONCAT(t.last_name, \", \", t.first_name, \" \", t.phone_number) AS winner,
        t.preference,
        b.winning_ticket,
        b.basket_id,
        b.basket_desc,
        b.basket_donor
        FROM `{self.basket_table}` AS b
        LEFT JOIN `{self.ticket_table}` AS t
        ON b.winning_ticket = t.ticket_id
        ORDER BY winner, b.basket_id"""
        cur.execute(create_str)
        conn.commit()
        conn.close()
    def select_range(self, start_num:int, end_num:int):
        conn, cur = session_maker()
        record_set = {}
        for i in range(start_num, end_num+1):
            record_set[i] = ""
        select_str = f"SELECT * FROM `{self.reportname}` WHERE basket_id BETWEEN {start_num} AND {end_num}"
        cur.execute(select_str)
        for i in cur.fetchall():
            record_set[i[3]] = i[0]
        conn.close()
        return record_set
    def select_all(self):
        conn, cur = session_maker()
        select_str = f"SELECT * FROM `{self.reportname}`"
        cur.execute(select_str)
        results = cur.fetchall()
        conn.close()
        return results
    def select_filtered(self, filter:str):
        conn, cur = session_maker()
        select_str = f"SELECT * FROM `{self.reportname}` WHERE {filter}"
        cur.execute(select_str)
        results = cur.fetchall()
        conn.close()
        return results
    def drop(self):
        conn, cur = session_maker()
        drop_str = f"DROP VIEW `{self.reportname}`"
        cur.execute(drop_str)
        conn.commit()
        conn.close()

class ReportByBasket():
    def __init__(self, prefix:str):
        self.reportname = f"{prefix}_r_bybasket"
        self.ticket_table = f"{prefix}_tickets"
        self.basket_table = f"{prefix}_baskets"
    def create(self):
        conn, cur = session_maker()
        create_str = f"""CREATE VIEW `{self.reportname}` AS
        SELECT b.basket_id,
        b.basket_desc,
        b.basket_donor,
        b.winning_ticket,
        CONCAT(t.last_name, \", \", t.first_name, \" \", t.phone_number) AS winner,
        t.preference
        FROM `{self.basket_table}` AS b
        LEFT JOIN `{self.ticket_table}` AS t
        ON b.winning_ticket = t.ticket_id
        ORDER BY b.basket_id"""
        cur.execute(create_str)
        conn.commit()
        conn.close()
    def select_all(self):
        conn, cur = session_maker()
        select_str = f"SELECT * FROM `{self.reportname}`"
        cur.execute(select_str)
        results = cur.fetchall()
        conn.close()
        return results
    def select_filtered(self, filter:str):
        conn, cur = session_maker()
        select_str = f"SELECT * FROM `{self.reportname}` WHERE {filter}"
        cur.execute(select_str)
        results = cur.fetchall()
        conn.close()
        return results
    def drop(self):
        conn, cur = session_maker()
        drop_str = f"DROP VIEW `{self.reportname}`"
        cur.execute(drop_str)
        conn.commit()
        conn.close()

class PrefixTable():
    def __init__(self):
        pass
    def create(self, prefix:str, bootstyle:str):
        ticket_table = TicketTable(prefix)
        basket_table = BasketTable(prefix)
        byname_view = ReportByName(prefix)
        bybasket_view = ReportByBasket(prefix)

        ticket_table.create()
        basket_table.create()
        byname_view.create()
        bybasket_view.create()

        conn, cur = session_maker()
        insert_str = f"""INSERT INTO prefixes (prefix, bootstyle) VALUES
        (\"{prefix}\", \"{bootstyle}\")"""
        cur.execute(insert_str)
        conn.commit()
        conn.close()
    def select(self, prefix:str):
        conn, cur = session_maker()
        select_str = f"""SELECT * FROM prefixes WHERE prefix=\"{prefix}\""""
        cur.execute(select_str)
        result = cur.fetchone()
        conn.close()
        if result:
            return (result[0], result[1])
        else:
            return "No Values"
    def select_all(self):
        conn, cur = session_maker()
        select_str = "SELECT * FROM prefixes"
        cur.execute(select_str)
        results = cur.fetchall()
        conn.close()
        return results
    def edit_bootstyle(self, prefix:str, bootstyle:str):
        conn, cur = session_maker()
        edit_str = f"UPDATE prefixes SET bootstyle = \"{bootstyle}\" WHERE prefix=\"{prefix}\""
        cur.execute(edit_str)
        conn.commit()
        conn.close()
    def drop(self, prefix:str):
        ticket_table = TicketTable(prefix)
        basket_table = BasketTable(prefix)
        byname_view = ReportByName(prefix)
        bybasket_view = ReportByBasket(prefix)

        byname_view.drop()
        bybasket_view.drop()
        basket_table.drop()
        ticket_table.drop()

        conn, cur = session_maker()

        drop_str = f"DELETE FROM prefixes WHERE prefix=\"{prefix}\""
        cur.execute(drop_str)
        conn.commit()
        conn.close()

class PermChecker:
    def __init__(self):
        pass
    def check_admin(self):
        conn, cur = session_maker()
        check = 0
        cur.execute("SHOW GRANTS")
        results = cur.fetchall()
        for i in results:
            if i[0].startswith(f"GRANT ALL PRIVILEGES ON `{conn.database}`.*"):
                check += 1
        conn.close()
        return check
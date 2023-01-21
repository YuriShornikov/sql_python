import psycopg2

def createdb(con):
    with con.cursor() as cur:

        cur.execute("""
        DROP TABLE phones;
        DROP TABLE clients;
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            name VARCHAR(60) NOT NULL,
            surname VARCHAR(60) NOT NULL,
            email VARCHAR NOT NULL
            );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            phone VARCHAR,
            client_id SERIAL NOT NULL REFERENCES clients(id)
            );
        """)

        con.commit()

def add_clients(con, name, surname, email, phone=None):
    with con.cursor() as cur:
        cur.execute("""
            INSERT INTO clients(name, surname, email) 
            VALUES(%s, %s, %s);""",
            (name, surname, email, )
        )

        cur.execute("""
            SELECT * FROM clients;"""
        )
        print(cur.fetchall())

        cur.execute("""
            INSERT INTO phones(phone)
            VALUES (%s);""",
            (phone, )
        )

        cur.execute("""
            SELECT * FROM phones;"""
        )
        print(cur.fetchall())

        con.commit()

def add_phone(con, client_id, phone):
    with con.cursor() as cur:
        cur.execute("""
            INSERT INTO phones(client_id, phone)
            VALUES (%s , %s);""",
            (client_id, phone, )
        )

        cur.execute("""
            SELECT * FROM phones;"""
        )
        print(cur.fetchall())

        con.commit()

def update_client(con, client_id, name, surname, email, phone, phone_change):
    with con.cursor() as cur:
        cur.execute("""
            UPDATE clients SET name = %s, surname = %s, email = %s
            WHERE id = %s;""",
            (name, surname, email, client_id, )
        )

        cur.execute("""
            SELECT * FROM clients;"""
        )
        print(cur.fetchall())

        cur.execute("""
            UPDATE phones SET phone = %s
            WHERE client_id = (
                SELECT p.client_id FROM phones p
                join clients c ON p.client_id = c.id
                WHERE c.name = %s
                limit 1) and phone = %s""",
            (phone, name, phone_change, )
        )

        cur.execute("""
            SELECT * FROM phones;
            """)

        print(cur.fetchall())

        con.commit()


def delete_phone(con, name, phone):
    with con.cursor() as cur:
        cur.execute("""
            DELETE FROM phones 
            WHERE client_id = (
                SELECT p.client_id FROM phones p
                join clients c ON p.client_id = c.id
                WHERE c.name = %s
                limit 1) and phone = %s;""",
            (name, phone, )
        )

        cur.execute("""
            SELECT * FROM phones;
            """)

        print(cur.fetchall())

        con.commit()

def delete_client(con, name):
    with con.cursor() as cur:
        cur.execute("""
            DELETE FROM phones 
            WHERE client_id = (
                SELECT p.client_id FROM phones p
                join clients c ON p.client_id = c.id
                WHERE c.name = %s
                limit 1);""",
            (name, )
            )

        cur.execute("""
            SELECT * FROM phones;"""
        )
        print(cur.fetchall())

        cur.execute("""
            DELETE FROM clients
            WHERE name = %s;""",
            (name, )
        )

        cur.execute("""
            SELECT * FROM clients;"""
        )
        print(cur.fetchall())

        con.commit()


def search_client(con, position):
    with con.cursor() as cur:
        cur.execute("""
            SELECT id FROM clients c
            WHERE c.id = (
                SELECT p.client_id FROM phones p
                JOIN clients c ON p.client_id = c.id
                WHERE p.phone = %s);""",
            (position,)
        )
        result = cur.fetchall()
        if len(result) > 0:
            print(result)

        cur.execute("""
            SELECT id FROM clients c
            WHERE c.name = %s;""",
            (position, )
        )
        result = cur.fetchall()
        if len(result) > 0:
            print(result)

        cur.execute("""
            SELECT id FROM clients c
            WHERE c.surname = %s;""",
            (position,)
        )
        result = cur.fetchall()
        if len(result) > 0:
            print(result)

        cur.execute("""
            SELECT id FROM clients c
            WHERE c.email = %s;""",
            (position,)
        )
        result = cur.fetchall()
        if len(result) > 0:
            print(result)


        con.commit()

if __name__ == '__main__':
    con = psycopg2.connect(database="sql_python", user="postgres", password="") #password - ваш пароль
    createdb(con)
    add_clients(con, name="test", surname="test", email="test@gmail.com", phone="77777") #добавляет клиента
    add_phone(con, client_id=1, phone="99999") #добавляет телефон
    update_client(con, client_id=1, name="test2", surname="test2", email="test2@gmail.com", phone="11111", phone_change="77777")
    delete_phone(con, name="test2", phone="11111") #удаление телефона клиента
    delete_client(con, name="test2") # удаление клиента
    search_client(con, position="test2@gmail.com") # поиск клиента, в данном случае я ищу id клиента, на место position можно подставить любое значение из задачи.

#в update_client, я добавил phone_chanhe в связи с тем, что у клиета может быть несколько телефонов и необходимо указать какой меняем

#delete_client надо закомитеть, иначе search_client не выполнить потом:)

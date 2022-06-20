import psycopg2
import cfg

HOST = cfg.HOST
PORT = cfg.PORT
DATABASE = cfg.DATABASE
USER = cfg.USER
PASSWORD = cfg.PASSWORD


def create_db(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer(
        id serial PRIMARY KEY,
        first_name varchar(100),
        last_name varchar(100),
        email varchar(100));

    CREATE TABLE IF NOT EXISTS phone(
        id serial PRIMARY KEY,
        number integer,
        customer_id integer not null REFERENCES customer(id));
    ''')
    conn.commit()


def insert_new_customer(cursor, first_name, last_name, email, number=0):
    cursor.execute('''
    INSERT INTO customer(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;
    ''', (first_name, last_name, email)
                   )
    if number > 0:
        cursor.execute('''
        INSERT INTO phone(number, customer_id) VALUES(%s, %s);
        ''', (number, cur.fetchone()[0])
                       )
    conn.commit()


def add_phone(cursor, customer_id, number):
    cursor.execute('''
    INSERT INTO phone(customer_id, number) VALUES(%s, %s);
    ''', (customer_id, number)
                   )
    conn.commit()


def delete_phones(cursor, customer_id):
    cursor.execute('''
    DELETE FROM phone WHERE customer_id = %s;
    ''', (customer_id,)
                   )
    conn.commit()


def change_customer(cursor, customer_id, first_name=None, last_name=None, email=None, phones=None):
    if first_name is not None:
        cursor.execute('''
        UPDATE customer SET first_name = %s WHERE id = %s;
        ''', (first_name, customer_id)
                       )
    if last_name is not None:
        cursor.execute('''
        UPDATE customer SET last_name = %s WHERE id = %s;
        ''', (last_name, customer_id)
                       )
    if email is not None:
        cursor.execute('''
        UPDATE customer SET email = %s WHERE id = %s;
        ''', (email, customer_id)
                       )
    if phones is not None:
        delete_phones(cursor, customer_id)
        for number in phones:
            add_phone(cursor, customer_id, number)

    conn.commit()


def delete_phone(cursor, customer_id, number):
    cursor.execute('''
    DELETE FROM phone WHERE customer_id = %s AND number = %s;
    ''', (customer_id, number)
                   )
    conn.commit()


def delete_customer(cursor, customer_id):
    delete_phones(cursor, customer_id)
    cursor.execute('''
    DELETE FROM customer WHERE id = %s;
    ''', (customer_id,)
                   )
    conn.commit()


def find_customer(cursor, first_name=None, last_name=None, email=None, phone=None):
    cursor.execute('''
    SELECT * FROM customer AS c
    JOIN phone AS p ON c.id = p.customer_id
    WHERE c.first_name = %s OR c.last_name = %s OR c.email = %s OR p.number = %s;
    ''', (first_name, last_name, email, phone)
                   )
    print(cur.fetchall())


conn = psycopg2.connect(host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD)

with conn.cursor() as cur:
    cur.execute('set search_path to apl_customers;')

    # Функция, создающая структуру БД (таблицы)
    create_db(cur)

    # Функция, позволяющая добавить нового клиента
    insert_new_customer(cur, 'Ivan', 'Ivanov', 'a@a.ru', 789456)
    insert_new_customer(cur, 'sdf', 'sdfd', 'as@sdfdfds.ru', 123456)
    insert_new_customer(cur, 'Petr', 'Petrov', 'petr@petrov.ru', 357951)

    # Функция, позволяющая добавить телефон для существующего клиента
    add_phone(cur, 2, 785236996)

    # Функция, позволяющая изменить данные о клиенте
    change_customer(cur, 3, first_name='Sidor', last_name='Sidorov', email='b@b.ru', phones=[654, 951356])

    # Функция, позволяющая удалить телефон для существующего клиента
    delete_phone(cur, 3, 951356)

    # Функция, позволяющая удалить существующего клиента
    delete_customer(cur, 3)

    # Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
    find_customer(cur, phone=789456)
    find_customer(cur, first_name='sdf')
conn.close()

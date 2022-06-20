import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import cfg
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import os
import json

BASE_PATH = os.getcwd()
TXT_DIR_NAME = 'fixtures'
file_name = 'tests_data.json'

HOST = cfg.HOST
PORT = cfg.PORT
DATABASE = cfg.DATABASE
USER = cfg.USER
PASSWORD = cfg.PASSWORD

DSN = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
engine = sqlalchemy.create_engine(DSN)


@event.listens_for(engine, "connect", insert=True)
def set_search_path(dbapi_connection, connection_record):
    existing_autocommit = dbapi_connection.autocommit
    dbapi_connection.autocommit = True
    cursor = dbapi_connection.cursor()
    cursor.execute("SET SESSION search_path=apl_book_store")
    cursor.close()
    dbapi_connection.autocommit = existing_autocommit


create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

full_path = os.path.join(BASE_PATH, TXT_DIR_NAME, file_name)
with open(full_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

for el in data:
    model = el['model']
    fields = el['fields']
    if model == 'publisher':
        md = Publisher(name=el['fields']['name'])
        session.add(md)
    elif model == 'book':
        md = Book(title=el['fields']['title'], id_publisher=el['fields']['publisher'])
        session.add(md)
    elif model == 'shop':
        md = Shop(name=el['fields']['name'])
        session.add(md)
    elif model == 'stock':
        md = Stock(id_book=el['fields']['book'], id_shop=el['fields']['shop'], count=el['fields']['count'])
        session.add(md)
    elif model == 'sale':
        md = Sale(price=el['fields']['price'], date_sale=el['fields']['date_sale'], count=el['fields']['count'],
                  id_stock=el['fields']['stock'])
        session.add(md)
session.commit()

publisher_id = int(input('Введите id издателя: '))
for c in session.query(Publisher).filter(Publisher.id == publisher_id).all():
    print(c)

session.close()

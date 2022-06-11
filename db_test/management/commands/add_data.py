from ast import Is
import pandas as pd
from db_test.models import Shoes
from sqlalchemy import create_engine
import time
# Create your tests here.




from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        # columns = list(range(0,800))
        # df = pd.read_csv('/Users/jujeonghan/Developer/did_it_walk/db_test/static/csv/cos_sim_eff_v2_l.csv', header = 0).iloc[:800,:800]
        # df.columns = columns
        # df.insert(0, 'id', pd.Series(columns))
        columns = ['id', 'tag_title', 'tag_price','tag_image_url']
        df = pd.read_csv('/Users/jujeonghan/Developer/did_it_walk/db_test/static/csv/shoes.csv', names=columns, header=0)
        engine = create_engine('sqlite://///Users/jujeonghan/Developer/did_it_walk/db.sqlite3')
        df.to_sql(Shoes._meta.db_table, if_exists='replace' ,con=engine, index=False)
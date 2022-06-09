import pandas as pd
from db_test.models import Shoes
from sqlalchemy import create_engine
# Create your tests here.




from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        columns = ['id', 'tag_title', 'tag_price','tag_image_url']
        df = pd.read_csv('/static/csv/shoes.csv', names=columns, header=0)

        engine = create_engine('sqlite:////db절대경로')
        df.to_sql(Shoes._meta.db_table, if_exists='replace' ,con=engine, index=False)
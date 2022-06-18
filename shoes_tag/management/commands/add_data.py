import pandas as pd
from post.models import ShoeTag
from itertools import islice
# Create your tests here.


from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        batch_size = 100
        columns = ['tag_title', 'tag_price','tag_image_url']
        df = pd.read_csv('/Users/jujeonghan/Developer/did_it_walk/shoes_tag/static/csv/shoes.csv', names=columns, header=0)
        objs = (ShoeTag(
            tag_title = row[0],
            tag_image_url = row[2]
        ) for _, row in df.iterrows())
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break
            ShoeTag.objects.bulk_create(batch, batch_size)
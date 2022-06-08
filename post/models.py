from distutils.command.upload import upload
from pyexpat import model
from django.db import models
from user.models import UserModel

# Create your models here.
class Shoe_tag(models.Model):
    class Meta:
        db_table = "Shoe_tag"
    tag_title = models.CharField(max_length=50)
    tag_price = models.IntegerField()
    tag_image_url = models.URLField("Site_URL")
    

class Post(models.Model):
    class Meta:
        db_table = "Post"
    contents = models.TextField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    shoe_tags = models.ManyToManyField(Shoe_tag, related_name='shoe_taggie')


class Post_Img(models.Model):
    class Meta:
        db_table = "Post_Img"
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    post_img = models.ImageField(upload_to="media/")


from django.db import models
from user.models import UserModel
from django.urls import reverse

# Create your models here.
class ShoeTag(models.Model):
    class Meta:
        db_table = "Shoe_tag"
    tag_title = models.CharField(max_length=50)
    tag_price = models.IntegerField()
    tag_image_url = models.URLField("Site_URL")
    

class Post(models.Model):
    class Meta:
        db_table = "Post"
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    post_img = models.ForeignKey('PostImg', on_delete=models.SET_NULL, null=True)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shoe_tags = models.ManyToManyField(ShoeTag, related_name='shoe_taggie')
    
    def get_absolute_url(self):
        return reverse("detail_page", kwargs={"pk": self.pk})
     

class PostImg(models.Model):
    class Meta:
        db_table = "Post_Img"
    post_img = models.ImageField(upload_to="media/")

class Likes(models.Model):
    class Meta:
        db_table = 'likes'
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True)
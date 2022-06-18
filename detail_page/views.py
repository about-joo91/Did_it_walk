import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from post.models import Post, ShoeTag, Comments, Likes
from shoes_tag.recommand_md import recommendation
# Create your views here.
class DetailView(APIView):
    """ 디테일페이지에 포스트 정보를 보내주는 APIView"""
    def get(self, request, pk):
        cur_user = request.user
        post = Post.objects.get(pk = pk)
        likes = len(Likes.objects.filter(post = post))
        is_like = Likes.objects.filter(post = post, user = cur_user).exists()
        shoe_tag = ShoeTag.objects.get(shoe_taggie = post)
        rd_shoes = recommendation.find_shoes_recommend(shoe_tag.id)
        recommend_shoe_tags = [ShoeTag.objects.get(id= str(rd_shoe)) for rd_shoe in rd_shoes]
        comments = Comments.objects.filter(post = post).order_by('-created_at')
        context = {
            'post' : post,
            'likes': likes,
            'is_like': is_like,
            'shoe_tag' : shoe_tag,
            'comments' : comments,
            'recommend_shoes' : recommend_shoe_tags,
        }
        return render(request, 'detail_page/detail_page.html', context)

class LikeView(APIView):
    """" 디테일 페이지 좋아요 기능"""
    def post(self, request,post_id):
        cur_user = request.user
        post = Post.objects.get(id= post_id)
        like_obj, create = Likes.objects.get_or_create(user= cur_user, post = post)
        
        if not create:
            like_obj.delete()
        else:
            pass
        return redirect('/detail_page/'+str(post_id))

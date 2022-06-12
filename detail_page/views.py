from django.shortcuts import render
from post.models import Post, ShoeTag, Comments, Likes
from shoes_tag.recommand_md import recommendation
# Create your views here.
def detail_page(request, pk):
    cur_user = request.user
    post = Post.objects.get(pk = pk)
    likes = Likes.objects.filter(post = post)
    is_like = Likes.objects.filter(post = post, user = cur_user).exists()
    shoe_tag = ShoeTag.objects.get(shoe_taggie = post)
    recommend = recommendation
    recommend_shoes = recommend.find_shoes_recommend(shoe_tag.id)
    recommend_shoe_tags = []
    for shoe in recommend_shoes:
        shoe_id = str(shoe)
        recommend_shoe_tags.append(ShoeTag.objects.get(id=shoe_id))
    comments = Comments.objects.filter(post = post).order_by('-created_at')
    context = {
        'post' : post,
        'likes': likes,
        'is_like': is_like,
        'shoe_tag' : shoe_tag,
        'comments' : comments,
        'recommend_shoes' : recommend_shoe_tags
    }
    return render(request, 'detail_page/detail_page.html', context)
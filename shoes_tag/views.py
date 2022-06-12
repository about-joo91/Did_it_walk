from django.shortcuts import render
from . import recommand_md
from post.models import ShoeTag
# Create your views here.
def recommend_shoes(request):
    shoe_tag_id = 1
    recommend = recommand_md.recommendation
    shoes = recommend.find_shoes_recommend(shoe_tag_id)
    shoe_tags= []
    for shoe in shoes:
        shoe_id = str(shoe)
        shoe_tags.append(ShoeTag.objects.get(id=shoe_id))
    cur_shoe_tag = ShoeTag.objects.get(id=1)
    return render(request, 'recommend_test/index.html',{'shoe_tags' : shoe_tags, 'cur_shoe_tag': cur_shoe_tag})

def get_specific_shoes(request):
    tag_id = request.POST.get('tag_id')
    recommend = recommand_md.recommendation
    shoes = recommend.find_shoes_recommend(tag_id)
    shoe_tags = []
    for shoe in shoes:
        shoe_id = str(shoe)
        shoe_tags.append(ShoeTag.objects.get(id=shoe_id))
    cur_shoe_tag = ShoeTag.objects.get(id=tag_id)
    return render(request, 'recommend_test/index.html', {'shoe_tags' : shoe_tags, 'cur_shoe_tag': cur_shoe_tag})
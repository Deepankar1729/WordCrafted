from .models import Category
from contact.models import SocialLink

def categories(request):
    categories = Category.objects.all()

    return{
        'categories': categories
    }

def social_links(request):
    links = SocialLink.objects.all()

    return{
        'links': links
    }
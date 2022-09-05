from . models import CompanyProfile, Type 

def company(request):
    cprofile = CompanyProfile.objects.get(pk=1)

    context = {
        'cprofile': cprofile,
    }

    return context 

def dropdown(request):
    category = Type.objects.all()

    context = {
        'category': category,
    }

    return context 
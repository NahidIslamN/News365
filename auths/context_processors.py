from apis.models import Category



def global_context(request):

    Categois = Category.objects.filter(status = True)


    return {
        'categoris': Categois if Categois else None,
    }
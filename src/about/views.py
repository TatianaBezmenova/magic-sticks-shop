from django.shortcuts import render

# url - view - model - view - template

def show_about(request):
    return render(request, 'about/about.html', {
        'name': 'Magick Sticks Shop',
    })

def show_mission(request):
    return  render(request, 'about/mission.html', {
        'name': 'Magick Sticks Shop',
    })



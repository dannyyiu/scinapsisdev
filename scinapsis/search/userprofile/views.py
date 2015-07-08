from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.models import User

from userprofile.models import UserProfile, PhoneModel, AddressModel


import logging

def _get_user_info(req):
    if req.user:
        return req.user
    else:
        return None

# Create your views here.
def index(request):

    user = _get_user_info(request)
    #profile, created = UserProfile.objects.get_or_create(user=user)
    #profile.middle_name = 'yoyoyo'
    #profile.save()
    context = {'user': user}
    return render(request, 'userprofile/view.html', context)

def profilepage(request):
    user = _get_user_info(request)
    if user is not None:
        context = {'user': user}
        return render(request, 'userprofile/profilepage.html', context)
    return redirect('userprofile:index')



def update_profile(request):
    user = _get_user_info(request)
    if user is not None:
        profile, profile_created = UserProfile.objects.get_or_create(user=user)
        profile.first_name = request.POST['first_name'].strip()
        profile.middle_name = request.POST['middle_name'].strip()
        profile.last_name = request.POST['last_name'].strip()

        if profile.phone is None:
            phone = PhoneModel.objects.create(phone_number=request.POST['phone_number'].strip())
            phone.save()
            profile.phone = phone
        else:
            profile.phone.phone_number = request.POST['phone_number'].strip()
            profile.phone.save()

        if profile.address is None:
            address = AddressModel.objects.create(street=request.POST['street_address'].strip(), province=request.POST['province_address'].strip(), country=request.POST['country_address'].strip())
            address.save()
            profile.address = address
        else:
            profile.address.street = request.POST['street_address'].strip()
            profile.address.province = request.POST['province_address'].strip()
            profile.address.country = request.POST['country_address'].strip()
            profile.address.save()

        profile.email = request.POST['email']

        if 'profile_image' in request.FILES:
            profile.image = request.FILES['profile_image']

        profile.save()

        return redirect('userprofile:profilepage')
    return redirect('userprofile:index')


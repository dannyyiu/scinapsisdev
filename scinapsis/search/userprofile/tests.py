from django.test import TestCase

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from userprofile.models import UserProfile, AddressModel, PhoneModel


# Create your tests here.
class UserProfileModelTests(TestCase):
    
    def test_make_a_user_and_profile(self):
        #create a new user: sinkpoint with password
        user = User.objects.create_user(username='abc', password='searchBYevidence99')
        user.save()
        
        #authenticate and get the new user back
        user2 = authenticate(username='abc', password='searchBYevidence99')
        
        self.assertTrue(user2 is not None)
        
        print UserProfile.objects.all()
        
        #create a new profile for this user
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        self.assertTrue(profile is not None)
        
        print UserProfile.objects.all()
        
        #put in profile information for fields except for the 'image' field
        profile.first_name = 'fname'
        profile.middle_name = 'mname'
        profile.last_name = 'lname'
        
        profile.email = 'sinkpoint@abcmail.com'
        
        #create an address object
        address = AddressModel(street='Unit 2125 Happy Street, Toronto',province='Ontario',country='Canada')
        
        #save it to the address table
        address.save()
        
        #put it into the profile
        profile.address = address
        
        #create a phone object
        phone = PhoneModel(phone_number='340958209')
        
        #save it to the phone table
        phone.save()
        
        #put it into the profile
        profile.phone = phone
        
        #save the profile new info
        profile.save()
        
        
        #get the profile through the user2
        user3 = User.objects.get(username='abc')
        
        #test if all the profile info saved
        self.assertEqual(user3.userprofile.first_name, 'fname')
        self.assertEqual(user3.userprofile.middle_name, 'mname')
        self.assertEqual(user3.userprofile.last_name, 'lname')
        self.assertTrue(user3.userprofile.address is not None)
        self.assertEqual(user3.userprofile.address.province, 'Ontario')
        self.assertEqual(user3.userprofile.email, 'sinkpoint@abcmail.com')
        self.assertEqual(user3.userprofile.phone.phone_number, '340958209')
        
        user_no_profile = User.objects.create_user(username='sdf', password='sdfa')
        user_no_profile.save()
        
        
        
        #print out existing profile objects, in which there should only be one object
        print UserProfile.objects.all()
        
        
        
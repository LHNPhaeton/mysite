from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)

    def __str__(self):
        return '%s for %s' %(self.nickname, self.user.username)




def has_nickname(self):
    return Profile.objects.filter(user=self).exists()

def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''

def get_username_or_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username

User.get_nickname = get_nickname
User.has_nickname = has_nickname
User.get_username_or_nickname = get_username_or_nickname



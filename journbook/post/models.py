from django.db import models
from accounts.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, blank=False)
    picture = models.ImageField(blank=True, upload_to='images/users/%Y/%m/%d', null=True)
    pub_date = models.DateTimeField(auto_now_add=True)

from django.db import models
from accounts.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    text = models.TextField(max_length=1000, blank=False)
    picture = models.ImageField(blank=True, upload_to='images/users/%Y/%m/%d', null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, default=None, blank=True)

    def __str__(self):
        return self.author.email

    @property
    def num_likes(self):
        return self.liked.all().count()

LIKE_CHOISES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOISES, default='Like', max_length=10000)

    def __str__(self):
        return str(self.post)
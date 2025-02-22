from django.db import models

class NewsPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post = models.ForeignKey(NewsPost, related_name='likes', on_delete=models.CASCADE)
    like_type = models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')], default=1)

    def __str__(self):
        return f"{self.user} {'liked' if self.like_type == 1 else 'disliked'} {self.post}"

class Comment(models.Model):
    post = models.ForeignKey(NewsPost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
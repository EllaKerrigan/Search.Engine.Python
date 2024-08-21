from django.db import models

# Create your models here.
from django.db import models


from django.db import models

class Post(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.TextField()
    url = models.TextField()
    permalink = models.TextField()
    subreddit = models.TextField()

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    id = models.AutoField(primary_key=True)  # Matches INTEGER PRIMARY KEY AUTOINCREMENT in SQLite
    post = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id')
    body = models.TextField()
    score = models.IntegerField()

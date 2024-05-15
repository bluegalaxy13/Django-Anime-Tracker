from django.db import models

class Anime(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	anime_name = models.CharField(max_length=50)
	genre = models.CharField(max_length=50)
	episodes = models.IntegerField()
	episodes_watched = models.IntegerField()
	rating = models.IntegerField()

	def __str__(self):
		return(f"{self.anime_name}")
 
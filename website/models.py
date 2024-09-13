from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Anime(models.Model):
    STATUS_CHOICES = [
        ('watching', 'Watching'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('plan_to_watch', 'Plan to Watch'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    anime_name = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    episodes = models.IntegerField()
    episodes_watched = models.IntegerField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.anime_name}"

    def clean(self):
        if self.episodes_watched > self.episodes:
            raise ValidationError("Episodes watched cannot be more than total episodes")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def mark_as_completed(self):
        self.episodes_watched = self.episodes
        self.status = 'completed'
        self.save()

    def get_absolute_url(self):
        return reverse('anime_detail', kwargs={'pk': self.pk})

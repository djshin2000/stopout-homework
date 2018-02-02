from django.db import models


class Webtoon(models.Model):
    webtoon_id = models.CharField(max_length=15)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.title} | {self.webtoon_id}'


class Episode(models.Model):
    webtoon = models.ForeignKey('Webtoon', on_delete=models.CASCADE)
    episode_id = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    rating = models.CharField(max_length=5)
    created_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} | {self.episode_id}'

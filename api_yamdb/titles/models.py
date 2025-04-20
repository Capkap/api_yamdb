from django.db import models

class Title(models.Model):
    rating = models.FloatField(null=True, blank=True)

    def update_average_rating(self):
        from django.db.models import Avg
        self.rating = self.reviews.aggregate(Avg('score'))['score__avg']
        self.save(update_fields=['rating'])

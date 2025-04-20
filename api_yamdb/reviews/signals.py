from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review, Title

@receiver([post_save, post_delete], sender=Review)
def update_title_rating(sender, instance, **kwargs):
    if not hasattr(instance, 'title'):
        return
    
    title = instance.title
    avg_rating = Review.objects.filter(title=title).aggregate(Avg('score'))['score__avg']
    
    Title.objects.filter(id=title.id).update(
        rating=round(avg_rating, 1) if avg_rating else None
    )

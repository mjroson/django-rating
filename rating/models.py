from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.core.mail import EmailMultiAlternatives

try:
    from django.contrib.contenttypes.generic import GenericForeignKey
except:
    from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.contenttypes.models import ContentType

from .managers import RatingManager

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)

CHOICES_STATUS = (
    (0, "Pendiente"),
    (1, "Aceptado"),
    (2, "Anulado")
)

CHOICES_VOTING = (
    (1, "Very bad"),
    (2, "Bad"),
    (3, "Medium"),
    (4, "Good"),
    (5, "Very Good")
)

class OverallRating(models.Model):
    # TODO: add unique "voted type" with "voted id",
    voted_type = models.ForeignKey(ContentType, related_name='overall_voted_type')
    voted_id = models.PositiveIntegerField()
    voted = GenericForeignKey('voted_type', 'voted_id')

    quantity_vote = models.PositiveIntegerField(default=0)
    rate = models.DecimalField(decimal_places=1, max_digits=6, null=True)

    def get_percent_rate(self):
        return float(self.rate / len(CHOICES_VOTING) * 100)

    @classmethod
    def update(self, rating):
        try:
            o_rating = OverallRating.objects.get(voted_id=rating.voted_id)
            o_rating.rate = Rating.objects.rating_all_by_voted(rating.voted_id)
            #o_rating.quantity_vote += 1
            o_rating.quantity_vote = Rating.objects.filter(voted_id=rating.voted_id, state=1).count()
            o_rating.save()
        except OverallRating.DoesNotExist:
            OverallRating(voted=rating.voted,
                          rate=Rating.objects.rating_all_by_voted(rating.voted_id),
                          quantity_vote= Rating.objects.filter(voted_id=rating.voted_id, state=1).count()
            ).save()
        except:
            print("Errors when update overallrating")


class Rating(models.Model):
    trans_type = models.ForeignKey(ContentType, related_name='transation_type')
    transaction_id = models.PositiveIntegerField()
    transaction_object = GenericForeignKey('trans_type', 'transaction_id')

    state = models.IntegerField(choices=CHOICES_STATUS, default=0)
    rate = models.PositiveIntegerField(null=True, choices=CHOICES_VOTING)
    created = models.DateTimeField(auto_now_add=True)
    voter = models.ForeignKey(USER_MODEL, related_name="user_voter")

    voted_type = models.ForeignKey(ContentType, related_name='voted_type')
    voted_id = models.PositiveIntegerField()
    voted = GenericForeignKey('voted_type', 'voted_id')

    objects = RatingManager.as_manager()

    def __str__(self):
        if self.rate:
            return 'Rating voted, Product is %s rate is %s' % (self.voted, self.rate)
        else:
            return "Rating waiting voter."

    def save(self, *args, **kwargs):
        if self.rate:
            self.state = 1

        return super(Rating, self).save(*args, **kwargs)


from commerce.order.models import Order

@receiver(post_save, sender=Order)
def init_rating(sender, *args, **kwargs):
    """
        Created instance rating when update status transaccion approved
    """
    if not kwargs['created']:
        order = kwargs['instance']
        #TODO : Solo ordenes de usuarios registrados pueden votar
        if order.status == 'shipped' and order.user:
            for item in order.get_items():

                Rating(transaction_object=order, voted=item.product , voter=order.user).save()





@receiver(post_save, sender=Rating)
def save_calification(sender, *args, **kwargs):
   """
       Send email when create rating and overall when rating voted
   """
   rating = kwargs['instance']
   if kwargs['created']:

       url = reverse('rating:califications2', kwargs={"trans_id": rating.transaction_id})
       message = 'Califica al usuario accediendo a ' + url

       msg = EmailMultiAlternatives('OwnCommerce - Notifications',
                                              message,
                                              'matiroson@gmail.com',
                                              [rating.voter.email])
       msg.attach_alternative(message, 'text/html')
       msg.send()
   else:
       if rating.rate:
           OverallRating.update(rating=rating)

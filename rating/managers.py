from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Avg


class RatingManager(models.QuerySet):

    def rating_all_by_voted(self, voted):
        return self.filter(voted_id=voted).aggregate(rating=Avg("rate"))['rating']

    def exists_rating(self, transaction):
        ct = ContentType.objects.get_for_model(transaction)

        if self.filter(transaction_id=transaction.id).filter(transaction_type=ct).count() == 0:
            return True
        else:
            return False
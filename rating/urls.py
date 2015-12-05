from django.conf.urls import patterns, url

from .views import ActionRatingView, manage_ratings

urlpatterns = patterns('',
                       url(r"^(?P<pk>[0-9]+)/$", ActionRatingView.as_view(), name="califications"),
                       url(r"^bulk/(?P<trans_id>[0-9]+)/$", manage_ratings, name="califications2"),
                        )

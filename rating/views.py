from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.forms.models import modelformset_factory
from django.http import HttpResponseNotAllowed
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from .forms import RatingForm
from .models import Rating

class ActionRatingView(UpdateView):
    model = Rating
    template_name = 'rating/form.html'
    form_class = RatingForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.voter == self.request.user and obj.state == 0:
            return super(ActionRatingView, self).dispatch(request, *args, **kwargs)

        return HttpResponseNotAllowed("No tienes permisos")


    def get_success_url(self):
        return reverse('home')


@login_required
def manage_ratings(request, trans_id):
    RatingFormSet = modelformset_factory(Rating, form=RatingForm, extra=0)
    if trans_id:
        ratings = Rating.objects.filter(transaction_id=trans_id, state=0)

        if ratings:
            if request.method == "POST":
                formset = RatingFormSet(request.POST, request.FILES,
                                        queryset=ratings)
                if formset.is_valid():
                    formset.save()
                    message = 'Gracias por votar!!'
                    return TemplateResponse(request,
                                            ["util/show_message.html",],
                                            { "show_messages": [ ('success', message), ],})
            else:
                formset = RatingFormSet(queryset=Rating.objects.filter(transaction_id=trans_id, state=0))

            return TemplateResponse(
                request, ['rating/rating_products_order.html',],
                {'formset': formset})
        else:
            message = 'Ya voto todos los productos de esta orden.'
    else:
        message = 'Error, la transaccion es incorrecta.'

    return TemplateResponse(request,
                            ["util/show_message.html",],
                            { "show_messages": [ ('warning', message), ],})


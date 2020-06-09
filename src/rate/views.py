from django.views.generic import ListView

from rate.models import Rate


class RateListView(ListView):
    template_name = 'rate-list.html'
    queryset = Rate.objects.all()

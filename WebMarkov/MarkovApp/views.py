from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from MarkovApp.models import SingleMarkov, MergedMarkov
from MarkovApp.forms import SingleMarkovForm


class Home(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # Send (up to) 5 Merged & Single Markovs to the template
        # FIXME: Think of ordering them
        context['single_markovs'] = SingleMarkov.objects.all()[:5]
        context['merged_markovs'] = MergedMarkov.objects.all()[:5]

        return context


class UploadSource(CreateView):
    template_name = 'upload_source.html'
    form_class = SingleMarkovForm

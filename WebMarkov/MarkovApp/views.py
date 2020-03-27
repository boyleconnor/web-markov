from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from MarkovApp.models import Source, SingleMarkov, MergedMarkov
from MarkovApp.forms import SourceForm, SingleMarkovForm, MergedMarkovForm


class Home(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # Send (up to) 5 Merged & Single Markovs to the template
        # FIXME: Think of ordering them
        context['sources'] = Source.objects.all()[:5]
        context['single_markovs'] = SingleMarkov.objects.all()[:5]
        context['merged_markovs'] = MergedMarkov.objects.all()[:5]

        return context


class UploadSource(CreateView):
    template_name = 'upload_source.html'
    form_class = SourceForm


class SourceDetail(DetailView):
    template_name = 'source_detail.html'
    model = Source

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        source_file = self.object.source_file
        context['first_ten_texts'] = [source_file.readline() for i in range(10)]
        return context


class SingleMarkovCreate(CreateView):
    template_name = 'singlemarkov_create.html'
    form_class = SingleMarkovForm


class SingleMarkovDetail(DetailView):
    template_name = 'singlemarkov_detail.html'
    model = SingleMarkov


class MergedMarkovCreate(CreateView):
    template_name = 'mergedmarkov_create.html'
    form_class = MergedMarkovForm


class MergedMarkovDetail(DetailView):
    template_name = 'mergedmarkov_detail.html'
    model = MergedMarkov

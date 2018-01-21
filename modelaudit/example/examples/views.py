from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse

from examples.forms import ExampleForm
from examples.models import Example


class ExampleFormViewMixin(object):

    form_class = ExampleForm
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('examples:detail', kwargs={'pk': self.object.pk})


class ExampleCreateView(ExampleFormViewMixin, CreateView):
    pass

example_create_view = ExampleCreateView.as_view()


class ExampleUpdateView(ExampleFormViewMixin, UpdateView):

    model = Example

example_update_view = ExampleUpdateView.as_view()


class ExampleDetailView(DetailView):

    model = Example
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history'] = self.object.audit_records.all()
        return context

example_detail_view = ExampleDetailView.as_view()

from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import FeedbackForm


def show_about(request):
    return render(request, 'about/about.html', {
        'name': 'Magick Sticks Shop',
    })


def show_mission(request):
    return render(request, 'about/mission.html', {
        'name': 'Magick Sticks Shop',
    })


class FeedbackFormView(FormView):
    template_name = 'about/feedback_form.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('order:my')

    def form_valid(self, form):
        feedback = form.save(commit=False)

        if not self.request.user.is_anonymous:
            feedback.user = self.request.user

        feedback.save()
        return super().form_valid(form)

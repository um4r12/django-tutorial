from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Question, Choice
# Create your views here.

# Each view is responsible for either:
# i. returning an HttpResponse object with any content
# ii. raising an exception (ex. Http 404)

# notice the similarities between index(...), detail(...) and results(...)
# they all involve retrieving data from db based on url params and then loads
# and renders a template.
# this is a common idiom, and we can use generic views in django to remove
# code redundancy

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#
#     # problematic b/c page design is hard-coded in the view;
#     # only way to modify page design is by modifying this loc
#     # instead, we want to seperate design from logic (i.e. python)
#     # output = ', '.join([q.question_text for q in latest_question_list])
#
#     # loads template, and passes it a mapping of template vars with objects
#     # template = loader.get_template('polls/index.html')
#     context = {'latest_question_list': latest_question_list, }
#     #     return HttpResponse(template.render(context, request))
#     # idiom: load template, fill context, render template & return as HttpRes
#     # shortcut: 'render(request, template, context)' as a shortcut for idiom
#     # render(...) returns an HttpResponse of template rendered with context
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     # checks if question exists, if so renders it, otherwise raises an error
#     # try:
#     #    question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # idiom: get(), raises Http404 if does not exist
#     # shortcut: get_object_or_404(model, arguments);
#     # also get_list_or_404() which uses filter instead of get()
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {'question': question}
#     return render(request, 'polls/results.html', context)

# Removed old functional views and replacing it with generic views
# generic views require the model to act on (i.e model = ...)
# ListView abstracts the concept of "display a list of objects"


class IndexView(generic.ListView):
    # ListView uses a generic template <app name>/<model name>_list.html
    # However, we can override it
    template_name = 'polls/index.html'
    # We also have to override the default context variable, <model>_list
    # ALternatively, we could have modified the template to be question_list
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

# DetailView abstracts the concept of "display a detail page for an object"
# DetailView expects the pk value captured from the URL to be called 'pk'


class DetailView(generic.DetailView):
    model = Question
    # DetailView uses a generic template <app name>/<model name>_detail.html
    # However, we can override it
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
                      'question': question,
                      'error_message': "You didn't select a choice.",
                      })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question_id,)))

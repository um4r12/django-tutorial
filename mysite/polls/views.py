from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Question
# Create your views here.

# Each view is responsible for either:
# i. returning an HttpResponse object with any content
# ii. raising an exception (ex. Http 404)


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # problematic b/c page design is hard-coded in the view;
    # only way to modify page design is by modifying this loc
    # instead, we want to seperate design from logic (i.e. python)
    # output = ', '.join([q.question_text for q in latest_question_list])

    # loads the template, and passes it a mapping of template vars with objects
    # template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list, }
    #     return HttpResponse(template.render(context, request))
    # idiom: load template, fill context, render template and return as HttpRes
    # shortcut: 'render(request, template, context)' as a shortcut for idiom
    # render(...) returns an HttpResponse of template rendered with context
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # checks if question exists, if so renders it, otherwise raises an error
    # try:
    #    question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # idiom: get(), raises Http404 if does not exist
    # shortcut: get_object_or_404(model, arguments);
    # also get_list_or_404() which uses filter instead of get()
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

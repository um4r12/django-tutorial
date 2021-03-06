from django.urls import path

from . import views

# adds a namespace to the urls so that any url names fall under the 'polls'
# namespace. If another url name is details, it can differentiate the two URl
# structures.
app_name = 'polls'

urlpatterns = [
               # angle brackets 'capture' part of the url and sends it as
               # an argument to the view functions.
               # ex: /polls/; the '/polls/' is stripped off
               # path('', views.index, name='index'), # old functional way
               # ex: /polls/5/; the '/polls/' is stripped off and only '5/'
               # is sent
               # detail(request=<HttpRequest object>, question_id=5)
               # path('<int:question_id>/', views.detail, name='detail'),
               # ex: /polls/5/results/; the '/polls/' is stripped off and only
               # '5/results/' is sent
               # results(request=<HttpRequest object>, question_id=5)
               # path('<int:question_id>/results/', views.results, name='results'),
               # ex: /polls/5/vote; the '/polls/' is stripped off and only
               # '5/vote/' is sent
               # vote(request=<HttpRequest object>, question_id=5)

               # url using generic views
               path('', views.IndexView.as_view(), name='index'),
               # changed <int:question_id> to <int:pk> why??
               # DetailView expects the pk value captured from
               # the URL to be called 'pk'
               path('<int:pk>/', views.DetailView.as_view(), name='detail'),
               path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
               path('<int:question_id>/vote/', views.vote, name='vote'),
              ]

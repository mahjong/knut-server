from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from knut_server.tests.models import Test

urlpatterns = patterns('',
    (r'^test_upload/$', 'knut_server.tests.views.test_upload'),
    (r'^test_list/$', 'knut_server.tests.views.test_list'),
    (r'^test_list_public/$', 'knut_server.tests.views.test_list_public'),
    (r'^test_delete/(?P<test_id>.*)/$', 'knut_server.tests.views.test_delete'),
    (r'^questions_download/$', 'knut_server.tests.views.questions_download'),
    (r'^answers_download/$', 'knut_server.tests.views.answers_download'),
    (r'^user_answers_download/$', 'knut_server.tests.views.user_answers_download'),
    (r'^results_upload/$', 'knut_server.tests.views.results_upload'),
    (r'^results_list/$', 'knut_server.tests.views.results_list'),
    (r'^categories/$', 'knut_server.tests.views.categories'),
    (r'^categories/(?P<category_id>.*)', 'knut_server.tests.views.category'),
    (r'^$', direct_to_template, {'template': 'index.html'}),
)

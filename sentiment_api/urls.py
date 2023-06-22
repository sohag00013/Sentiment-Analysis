from django.urls import path

from . import views
#from sentiment_api.views import large_text_area

urlpatterns = [
    path("nlp", views.preprocess_index, name="preprocess_index"),
    path("", views.home, name="home"),
]
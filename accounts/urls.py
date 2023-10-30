from . import views
from school.urls import router as school_router
from finance.urls import router as finance_router
from finance import views as finviews
from .router import router
from .token import urlpatterns as token_url

from djoser.urls import authtoken
from django.urls import path


urlpatterns = [
    path("general_statistics/",views.General_Statistics.as_view()),
    path("finance/data/",finviews.Data_Finance.as_view())
]

urlpatterns+=router.urls
urlpatterns += school_router.urls
urlpatterns += finance_router.urls
# urlpatterns += authtoken.urlpatterns
urlpatterns += token_url
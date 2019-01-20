"""
vochabular URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin

from graphene_django.views import GraphQLView
from vochabular.schema import schema as auth
from api.schema import schema as api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api', GraphQLView.as_view(graphiql=True, schema=api)),
    url(r'^auth', GraphQLView.as_view(graphiql=True, schema=auth)),
]

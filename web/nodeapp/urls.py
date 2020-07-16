from django.conf.urls import url
from .views import GetNodesView

view_urls = [
    url(r'^get_nodes', GetNodesView.as_view(), name='get_nodes_func'),
]
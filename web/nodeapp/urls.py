from django.conf.urls import url
from .views import GetNodesView, LogsView

view_urls = [
    url(r'^get_nodes', GetNodesView.as_view(), name='get_nodes_func'),
    url(r'^logs', LogsView.as_view(), name='logs'),
]
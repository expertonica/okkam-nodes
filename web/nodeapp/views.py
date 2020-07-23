import json

from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .mappers import map_get_nodes
from .nodes import calculate_nodes

class GetNodesView(APIView):
    def get(self, request):
        return Response({'some_data': 'json'})

    def post(self, request):
        json_data = json.loads(request.body)
        query, companies = map_get_nodes(json_data)

        nodes = calculate_nodes(query, companies)
        node_list = []
        for N in nodes:
            node_list.append(nodes[N])

        return Response({'nodes': node_list})

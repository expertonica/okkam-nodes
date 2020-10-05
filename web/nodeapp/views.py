import json
import os
import glob
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from .mappers import map_get_nodes
from .nodes import calculate_nodes
from .mask import create_mask

class GetNodesView(APIView):
    def get(self, request):
        return Response({'some_data': 'json'})

    def post(self, request):
        json_data = json.loads(request.body)
        query, companies = map_get_nodes(json_data)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        logs_fname = os.path.join('logs', query+'.txt')
        with open(logs_fname, 'w') as f:
            json_object = json.dumps(json_data, indent=4)
            f.write(json_object)

        nodes = calculate_nodes(query, companies)
        node_list = []
        for N in nodes:
            node_list.append(nodes[N])

        if settings.USE_MASK:
            a = create_mask(query, nodes, companies)
        #return Response({'nodes': a})
        return Response({'nodes': node_list})

class LogsView(APIView):
    def get(self, request):
        search_dir = "media_root/"
        files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        for i in range(len(files)):
            files[i] = files[i].replace('media_root/', '')

        return render(request, 'index.html', {
            'files': files
        })

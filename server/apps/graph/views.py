from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from .models import Node, NodeRelation
from .serializers import NodeSerializer, NodeRelationSerializer


# Create your views here.
class GraphView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        nodes = Node.objects.all()
        nodes_serializer = NodeSerializer(nodes, many=True)

        edges = NodeRelation.objects.all()
        edges_serializer = NodeRelationSerializer(edges, many=True)

        return Response({'nodes': nodes_serializer.data, 'edges': edges_serializer.data})


class NodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, node_id=None, format=None):
        if node_id:
            node = get_object_or_404(Node, id=node_id)
            serializer = NodeSerializer(node)
            return Response(serializer.data)
        else:
            nodes = Node.objects.all()
            serializer = NodeSerializer(nodes, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, node_id, format=None):
        node = get_object_or_404(Node, id=node_id)
        serializer = NodeSerializer(node, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, node_id, format=None):
        node = get_object_or_404(Node, id=node_id)
        node.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NodeRelationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, relation_id=None, format=None):
        if relation_id:
            relation = get_object_or_404(NodeRelation, id=relation_id)
            serializer = NodeRelationSerializer(relation)
            return Response(serializer.data)
        else:
            relations = NodeRelation.objects.all()
            serializer = NodeRelationSerializer(relations, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NodeRelationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, relation_id, format=None):
        relation = get_object_or_404(NodeRelation, id=relation_id)
        serializer = NodeRelationSerializer(relation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, relation_id, format=None):
        relation = get_object_or_404(NodeRelation, id=relation_id)
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

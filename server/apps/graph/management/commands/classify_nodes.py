from django.core.management.base import AppCommand
from apps.graph.models import Node, NodeRelation


# Название класса обязательно - "Command"
class Command(AppCommand):
    # Используется как описание команды обычно
    help = 'Fond questions with zero true answers'

    def handle(self, *args, **kwargs):

        nodes = Node.objects.all()

        final_nodes = []
        start_nodes = []
        alone_nodes = []

        for node in nodes:
            edges_parent = NodeRelation.objects.filter(parent=node)
            edges_child = NodeRelation.objects.filter(child=node)

            if len(edges_parent) == 0:
                final_nodes.append(node.pk)
                if len(edges_child) == 0:
                    alone_nodes.append(node.pk)
            if len(edges_child) == 0:
                start_nodes.append(node.pk)

        print(f"Start nodes: {start_nodes}")
        print(f"Final nodes: {final_nodes}")
        print(f"Alone nodes: {alone_nodes}")

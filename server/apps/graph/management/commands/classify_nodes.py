from django.core.management.base import AppCommand
from apps.graph.models import Node, NodeRelation
from apps.questions.models import Question


# Название класса обязательно - "Command"
class Command(AppCommand):
    # Используется как описание команды обычно
    help = 'Fond questions with zero true answers'

    def handle(self, *args, **kwargs):

        nodes = Node.objects.all()

        final_nodes = []
        start_nodes = []
        alone_nodes = []
        nodes_without_questions = []

        for node in nodes:
            edges_parent = NodeRelation.objects.filter(parent=node)
            edges_child = NodeRelation.objects.filter(child=node)
            
            if node.testability == True:
                q_exist = node.questions_exist()
                if q_exist == 0:
                    nodes_without_questions.append(node.pk)

            if len(edges_parent) == 0:
                final_nodes.append(node.pk)
                if len(edges_child) == 0:
                    alone_nodes.append(node.pk)
            if len(edges_child) == 0:
                start_nodes.append(node.pk)

        print(f"Start nodes: {start_nodes}")
        print(f"Final nodes: {final_nodes}")
        print(f"Alone nodes: {alone_nodes}")
        print(f"Nodes without questions: {nodes_without_questions}")

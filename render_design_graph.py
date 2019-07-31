import io
import os

import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from graphviz import Digraph


def load_graph_yaml():
    with io.open("chat-design.yaml", mode="r", encoding="utf-8") as file:
        data = yaml.load(file, Loader)
    system = data['system']
    user_query = data['user_query']
    return system, user_query


def render_graph(system, user_query):
    dot = Digraph(
        node_attr=dict(shape='box', style='rounded, filled'),
        graph_attr=dict(splines='ortho'),
    )

    # Nodes
    render_nodes(dot, system, '#deebff')
    render_nodes(dot, user_query, '#ffebcc')

    # Edges
    render_edges(dot, system)
    render_edges(dot, user_query)

    file = "chatbot-design"
    file_format = 'svg'
    dot.format = file_format
    dot.render(file, cleanup=True, view=False)
    return f"{file}.{file_format}"


def render_edges(dot, system):
    for number, step in system.items():
        for to in step.get('to', []):
            dot.edge(f"{number}", f"{to}")


def render_nodes(dot, nodes, color):
    for number, step in nodes.items():
        dot.node(
            f"{number}",
            get_node_content(step),
            color=color,
        )


def get_node_content(step):
    parts = []
    if 'name' in step:
        parts.append(f"<b>{step['name']}</b>")
    if 'text' in step:
        text = step["text"].replace('\n', '<br/>')
        parts.append(f'<font point-size="9">{text}</font>')
    return (
            "<"
            + "<br/><br/>".join(parts)
            + ">"
    )


if __name__ == '__main__':
    output_file = render_graph(*load_graph_yaml())
    os.startfile(output_file)

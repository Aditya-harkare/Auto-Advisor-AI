from graph.workflow import workflow
import grandalf

graph = workflow.get_graph()

print(graph.draw_ascii())
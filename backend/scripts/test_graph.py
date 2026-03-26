from backend.app.services.graph_builder import build_graph

G = build_graph()

print("Total nodes:", len(G["nodes"]))
print("Total edges:", len(G["links"]))

for node in G["nodes"][:20]:
    print("Node:", node)

for edge in G["links"][:20]:
    print("Edge:", edge)
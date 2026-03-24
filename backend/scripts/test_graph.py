from backend.app.services.graph_builder import build_graph

G = build_graph()

print("Total nodes:", len(G.nodes))
print("Total edges:", len(G.edges))

# show sample
for node in list(G.nodes)[:20]:
    print("Node:", node)

for edge in list(G.edges(data=True))[:70]:
    print("Edge:", edge)
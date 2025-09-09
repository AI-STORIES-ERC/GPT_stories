import networkx as nx
import matplotlib.pyplot as plt

"""
This script generates a story flowchart based on an analysis of the Norwegian stories
that is hardcoded into the script.
It does not automatically identify the plotline, it is just a visualisation of provided data.
At this point it is written for the Norwegian stories in the GPT-stories dataset,
though it may be developed to work more generally in the future.

The script creates a file saved as "analysis/figures/story_flowchart.png"
"""

def create_story_flowchart(protagonist_names, instigating_events, quest_giver_locations, opponents):
    G = nx.DiGraph()
    pos = {}

    # Define the fixed nodes (with updated labels)
    nodes = {
        "setting": "In a small village by\nthe fjord/mountain",
        "the_protagonist": "the protagonist",
        "journey": "explores the forest and",
        "quest-giver": "finds its guardian spirit in",
        "conflict": "The guardian warns of\nconflict between nature and",
        "restore_balance": "Must restore balance by",
        "restoration_community": "Organising community",
        "restoration_personal": "Coming to terms with self",
        "village_future": "Village becomes a beacon\nof eco-sustainability/unity/courage"
    }

    # Add fixed nodes to the graph
    for key, label in nodes.items():
        G.add_node(key, label=label)

    # Function to evenly spread multiple child nodes, handling both fixed and dynamic nodes
    def spread_nodes(parent, children, y_level, x_center=0, x_spacing=1.5, use_labels=False):
        num_children = len(children)
        if num_children == 1:
            x_positions = [x_center]  # Center if only one child
        else:
            x_positions = [x_center + x_spacing * (i - (num_children - 1) / 2) for i in range(num_children)]  # Spread evenly
        
        for i, child in enumerate(children):
            label = nodes.get(child, child)  # Use predefined label if available, otherwise use the name
            G.add_node(child, label=label)
            G.add_edge(parent, child)
            pos[child] = (x_positions[i], y_level)

    # Spread protagonist names below "setting"
    spread_nodes("setting", protagonist_names, y_level=-0.5)

    # Connect protagonists to "The Protagonist"
    for name in protagonist_names:
        G.add_edge(name, "the_protagonist")

    # Position "The Protagonist" centrally below protagonists
    pos["the_protagonist"] = (0, -1.5)

    # Spread instigating events below "The Protagonist"
    spread_nodes("the_protagonist", instigating_events, y_level=-2.5, x_spacing=2)

    # Connect instigating events to "journey"
    for event in instigating_events:
        G.add_edge(event, "journey")

    # Spread quest-giver locations below "quest-giver"
    spread_nodes("quest-giver", quest_giver_locations, y_level=-5)

    # Connect quest-giver locations to conflict
    for location in quest_giver_locations:
        G.add_edge(location, "conflict")

    # Spread dynamic opponents below "conflict"
    spread_nodes("conflict", opponents, y_level=-7)

    # Connect each opponent to "restore_balance"
    for opponent in opponents:
        G.add_edge(opponent, "restore_balance")

    # **Move restorations further down**
    spread_nodes("restore_balance", ["restoration_community", "restoration_personal"], y_level=-9, x_spacing=2, use_labels=True)

    # Connect final restoration options to village future
    G.add_edge("restoration_community", "village_future")
    G.add_edge("restoration_personal", "village_future")

    # Define remaining fixed edges
    edges = [
        ("journey", "quest-giver"),
        ("quest-giver", "conflict")
    ]
    G.add_edges_from(edges)

    # Adjust fixed node positions for better spacing
    pos.update({
        "setting": (0, 0),
        "journey": (0, -3.2),
        "quest-giver": (0, -4.2),
        "conflict": (0, -6.2),
        "restore_balance": (0, -8.2),  # Now a clear decision point
        "village_future": (0, -11)  # Pulled up for balance
    })

    # Draw the graph
    plt.figure(figsize=(10, 12))
    labels = nx.get_node_attributes(G, "label")
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color="lightblue", edge_color="gray", font_size=12, font_weight="bold", arrows=True)
    

    plt.title("Story Flowchart (Restorations Moved Below 'Restore Balance')")

    #save to file "figures/story_flowchart.png"
    plt.savefig("analysis/figures/story_flowchart.png")
    plt.show(block=False)
    return G, pos

#generate an excel sheet with two columns: source and target based on this network
import pandas as pd
def generate_excel_from_graph(G, filename="analysis/data/story_flowchart_edges.xlsx"):
    edges = G.edges()
    df = pd.DataFrame(edges, columns=["Source", "Target"])
    df.to_excel(filename, index=False)

# Call this function after creating the graph in create_story_flowchart
def create_story_flowchart_with_excel(protagonist_names, instigating_events, quest_giver_locations, opponents):
    G, pos = create_story_flowchart(protagonist_names, instigating_events, quest_giver_locations, opponents)
    generate_excel_from_graph(G)


if __name__ == "__main__":

    protagonist_list = ["Freya", "Astrid", "Ingrid", "Elin"]
    instigating_event_list = ["returns home \nfrom Oslo and", "is an adventurous\nlocal girl who"]
    quest_giver_locations = ["a clearing in\nthe forest", "a rune-carved box", "an ancient tree"]
    opponents_list = ["people", "darkness", "extreme weather", "outsiders", "developers"]

    create_story_flowchart(protagonist_list, instigating_event_list, quest_giver_locations, opponents_list)
    #create_story_flowchart_with_excel(protagonist_list, instigating_event_list, quest_giver_locations, opponents_list)

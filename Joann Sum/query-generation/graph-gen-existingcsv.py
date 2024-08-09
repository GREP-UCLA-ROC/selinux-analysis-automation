#you need to have a neo4j instance running. You can make one locally or with neo4j aura. Replace the URI and enter the correct username and password to connect.
#import your csvs (generated from running the bash script from the previous section 'parser-selinux.sh') into the neo4j from the console or in your local instance. This will save time. Or you can run:
#'python graph-generation.py'

import sys
from neo4j import GraphDatabase
import matplotlib.pyplot as plt
import networkx as nx
from tqdm import tqdm

def visualize_graph(driver, rule_type):
    print(f"\nVisualizing graph for {rule_type} rules...")

    query = f"""
    MATCH (s:Type)-[r:ACCESS {{type: '{rule_type}'}}]->(t:Type)-[:OF_CLASS]->(c:Class)
    RETURN s, r, t, c LIMIT 1000
    """
    
    with driver.session() as session:
        result = session.run(query)
        
        G = nx.DiGraph()  # Change to DiGraph instead of MultiDiGraph
        
        print("Processing graph data...")
        edge_labels = {}
        for record in tqdm(result):
            source = record['s']
            target = record['t']
            relation = record['r']
            class_node = record['c']
            
            G.add_node(source['name'], label=source['name'], node_type='Type')
            G.add_node(target['name'], label=target['name'], node_type='Type')
            G.add_node(class_node['name'], label=class_node['name'], node_type='Class')
            
            edge_key = (source['name'], target['name'])
            edge_label = f"{relation['type']}\n{','.join(relation['permissions'])}"
            
            if edge_key in edge_labels:
                edge_labels[edge_key] += f"\n{edge_label}"
            else:
                edge_labels[edge_key] = edge_label
            
            G.add_edge(source['name'], target['name'])
            G.add_edge(target['name'], class_node['name'], label='OF_CLASS')

    print("Generating layout...")
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    plt.figure(figsize=(20,20))
    
    print("Drawing graph...")
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    
    plt.title(f"SELinux Policy Graph - {rule_type.capitalize()} Rules")
    plt.axis('off')
    plt.tight_layout()
    
    print(f"Saving graph as selinux_policy_graph_{rule_type}.png...")
    plt.savefig(f"selinux_policy_graph_{rule_type}.png")
    plt.close()

    print(f"Graph visualization for {rule_type} rules completed.")

def run_custom_query(driver, query):
    print("\nRunning custom query...")
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]

def main(username, password):
    URI = "neo4j+s://4d1c6765.databases.neo4j.io:7687"
    
    with GraphDatabase.driver(URI, auth=(username, password)) as driver:
        # Visualize graphs for allow and dontaudit rules
        for rule_type in ['allow', 'dontaudit']:
            visualize_graph(driver, rule_type)

        # Example of a custom query
        custom_query = """
        MATCH (s:Type)-[r:ACCESS]->(t:Type)
        WHERE r.permissions CONTAINS 'write'
        RETURN s.name AS Source, t.name AS Target, r.type AS RuleType
        LIMIT 10
        """
        results = run_custom_query(driver, custom_query)
        print("\nCustom Query Results:")
        for record in results:
            print(f"Source: {record['Source']}, Target: {record['Target']}, Rule Type: {record['RuleType']}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <neo4j_username> <neo4j_password>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    main(username, password)
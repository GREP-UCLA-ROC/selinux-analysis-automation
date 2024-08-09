import sys
from neo4j import GraphDatabase
import matplotlib.pyplot as plt
import networkx as nx
from tqdm import tqdm

def run_query_and_visualize(driver, query, title, filename):
    print(f"\nRunning query: {title}")
    
    with driver.session() as session:
        result = session.run(query)
        
        G = nx.DiGraph()
        
        print("Processing query results...")
        for record in tqdm(result):
            for item in record.values():
                if hasattr(item, 'start_node'):  # Relationship
                    start_node = item.start_node
                    end_node = item.end_node
                    G.add_node(start_node['name'], label=start_node['name'], node_type=list(start_node.labels))
                    G.add_node(end_node['name'], label=end_node['name'], node_type=list(end_node.labels))
                    G.add_edge(start_node['name'], end_node['name'], 
                               label=f"{item.type}\n{','.join(item.get('permissions', []))}")
                elif hasattr(item, 'labels'):  # Node
                    G.add_node(item['name'], label=item['name'], node_type=list(item.labels))

    if G.number_of_nodes() == 0:
        print("No results found for this query.")
        return

    print("Generating layout...")
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    plt.figure(figsize=(20,20))
    
    print("Drawing graph...")
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    
    print(f"Saving graph as {filename}")
    plt.savefig(filename)
    plt.close()


def main(username, password):
    URI = "neo4j+s://4d1c6765.databases.neo4j.io:7687"
    
    queries = [
        {
            "title": "Separation of Duty Violation",
            "query": """
            MATCH (s:Type)-[r1:ACCESS]->(t:Type)<-[r2:ACCESS]-(s)
            WHERE r1.permissions CONTAINS 'read' AND r2.permissions CONTAINS 'write'
            RETURN s, t, r1, r2
            LIMIT 100
            """,
            "filename": "separation_of_duty_violation.png"
        },
        {
            "title": "Contradictions",
            "query": """
            MATCH (s:Type)-[r1:ACCESS]->(t:Type), (s)-[r2:ACCESS]->(t)
            WHERE r1.type = 'allow' AND r2.type = 'dontaudit'
            AND any(perm IN r1.permissions WHERE perm IN r2.permissions)
            RETURN s, t, r1, r2
            LIMIT 100
            """,
            "filename": "contradictions.png"
        },
        {
            "title": "Missing Domain Transition Rules",
            "query": """
            MATCH (s:Type)-[r:ACCESS {type: 'allow'}]->(t:Type)
            WHERE 'transition' IN r.permissions
            AND NOT EXISTS {
                MATCH (s)-[r2:ACCESS {type: 'allow'}]->(e:Type)
                WHERE 'entrypoint' IN r2.permissions
            }
            RETURN s, t, r
            LIMIT 100
            """,
            "filename": "missing_domain_transition.png"
        },
        {
            "title": "Missing Rules (Objects without Allow Access)",
            "query": """
            MATCH (t:Type)
            WHERE NOT EXISTS {
                MATCH (s:Type)-[:ACCESS {type: 'allow'}]->(t)
            }
            RETURN t
            LIMIT 100
            """,
            "filename": "missing_rules.png"
        },
        {
            "title": "Overly Permissive Rules",
            "query": """
            MATCH (s:Type)-[r:ACCESS {type: 'allow'}]->(t:Type)
            WHERE size(r.permissions) > 5
            RETURN s, t, r
            LIMIT 100
            """,
            "filename": "overly_permissive_rules.png"
        }
    ]

    with GraphDatabase.driver(URI, auth=(username, password)) as driver:
        for query_info in queries:
            run_query_and_visualize(driver, query_info["query"], query_info["title"], query_info["filename"])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <neo4j_username> <neo4j_password>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    main(username, password)
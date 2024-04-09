from neo4j_classes import Neo4jConnection
from neo4jconfig import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, BASE_URL

# Neo4j connection parameters
uri = NEO4J_URI  
username = NEO4J_USERNAME        
password = NEO4J_PASSWORD
base_url = BASE_URL

def main():
    # Connect to Neo4j
    connection = Neo4jConnection(uri, username, password)

    queries = [
        # f"""
        # LOAD CSV WITH HEADERS FROM '{base_url}/Node_affiliation.csv' AS row
        # MERGE (a:Affiliation {{name: row.name, type: row.type}})
        # """,

        # f"""
        # LOAD CSV WITH HEADERS FROM '{base_url}/Edge_author_affiliation.csv' AS row
        # MATCH (a:Author {{name: row.author}})
        # MATCH (b:Affiliation {{name: row.name}})
        # MERGE (a)-[r:belongs_to]->(b);
        # """,

        # # Add properties to reviews
        # f"""
        # MATCH (p:Paper)-[r:reviews]-(a:Author)
        # SET r.approves=TRUE
        # RETURN r
        # """,
    ]  

    # Execute each query, respecting the readable formatting
    for i, query in enumerate(queries, start=1):
        print(f"Executing Query {i}...")
        connection.load_csv_data(query)

    connection.close()

if __name__ == '__main__':
    main()
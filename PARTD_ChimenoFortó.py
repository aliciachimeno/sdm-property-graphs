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
        """
        CALL gds.pageRank.stream('pageRankGraph', {maxIterations: 50,dampingFactor: 0.85}) YIELD nodeId, score
        RETURN gds.util.asNode(nodeId).name AS title, score 
        ORDER BY score DESC, title DESC
        limit 10;
        """
    ]

    connection.execute_queries_and_print_results(queries)

    connection.close()

if __name__ == '__main__':
    main()
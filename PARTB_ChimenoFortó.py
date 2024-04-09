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
     
    # Queries to execute, formatted for readability
    queries = [
        """
        MATCH (c:Conference)--()--(p2:Papers)<--(p:Papers)
        WITH c, p2, count(p) as numCitations
        order by numCitations desc
        with c.name as Conference, collect({Paper:p2.name, numOfCitations:numCitations}) as citations
        return Conference,citations[0..3] as TOP3
        order by Conference
        """,
    ]

    connection.execute_queries_and_print_results(queries)

    connection.close()

if __name__ == '__main__':
    main()

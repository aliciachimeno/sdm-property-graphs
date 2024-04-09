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
        MATCH (c:Conference)--()--(p2:Papers)<--(p1:Papers)
        WITH c, p2, count(p1) AS numCitations
        ORDER BY numCitations DESC
        WITH c.name AS Conference, COLLECT({Paper:p2.name, NumOfCitations:numCitations}) AS citations
        RETURN Conference, citations[0..3] AS TOP3
        ORDER BY Conference
        """,

        """
        MATCH (c:Conference)--(e:Edition)--(p:Papers)<-[:writes]-(a:Author)
        WITH a, c, count(distinct e) AS numOfEditions
        WHERE numOfEditions >= 4
        RETURN a.name, c.name, numOfEditions
        ORDER BY numOfEditions DESC
        """,

        """
        MATCH (j:Journal)--(v:Volume)--(p:Papers)
        WITH j, v.year AS publicationYear, count(p) AS numOfPublications

        MATCH (j:Journal)--(cited_v:Volume)--(cited_p:Papers)<-[c:cites]-(citing_p:Papers)--(citing_v:Volume)
        WHERE cited_v.year = citing_v.year - 1 OR cited_v.year = citing_v.year - 2
        WITH j, toInteger(citing_v.year) AS citationYear, count(c) AS numOfCitations, publicationYear, numOfPublications
        WHERE  publicationYear = citationYear - 1 OR publicationYear = citationYear - 2

        WITH j, citationYear, sum(numOfPublications) AS totalPublications, numOfCitations
        RETURN j.name AS Journal, citationYear AS Year, numOfCitations / totalPublications AS ImpactFactor
        ORDER BY j.name, citationYear
        """
    ]

    connection.execute_queries_and_print_results(queries)

    connection.close()

if __name__ == '__main__':
    main()

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
     
    loading_queries = [
        #STAGE 1
        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Node_community.csv' AS row
        MERGE (a:Community {{name: row.community}})
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Edge_community_keyword.csv' AS row
        MATCH (a:Community {{name: row.community}})
        MATCH (b:Keywords {{name: row.keywords}})
        MERGE (a)-[r:associated_with]->(b);
        """
    ]
    queries = [
        #STAGE 2
        """
        MATCH (j:Journal)--()--(p:Papers) 
        WITH j, count(DISTINCT p) AS total_journal_papers

        MATCH (j)--()--(p1:Papers)--()--(c:Community {name:"Database"})
        WITH j, total_journal_papers, count(DISTINCT p1) AS db_journal_papers
        WITH j, toFloat(db_journal_papers) / toFloat(total_journal_papers) AS percentage 
        WHERE percentage >= 0.9
        CREATE (j)-[:belongs_to]->(:Community {name: "Database"})
        RETURN j.name AS name, 'Journal' AS type, percentage
        UNION
        MATCH (co:Conference)--()--(p:Papers) 
        WITH co, count(DISTINCT p) AS total_conference_papers

        MATCH (co)--()--(p2:Papers)--()--(c:Community {name:"Database"})
        WITH co, total_conference_papers, count(DISTINCT p2) AS db_conference_papers
        WITH co, toFloat(db_conference_papers) / toFloat(total_conference_papers) AS percentage 
        WHERE percentage >= 0.9
        CREATE (co)-[:belongs_to]->(:Community {name: "Database"})
        RETURN co.name AS name, 'Conference' AS type, percentage;
        """,
        #STAGE 3

    ]
    for i, loading_queries in enumerate(loading_queries, start=1):
        print(f"Executing Query {i}...")
        connection.load_csv_data(loading_queries)

    connection.execute_queries_and_print_results(queries)

    connection.close()

if __name__ == '__main__':
    main()
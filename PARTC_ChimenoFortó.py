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
        """,
        #STAGE 2
        """
        MATCH (j:Journal)--()--(p:Papers) 
        WITH j, count(DISTINCT p) AS total_journal_papers

        MATCH (j)--()--(p1:Papers)--()--(c:Community {name:"Database"})
        WITH c,j, total_journal_papers, count(DISTINCT p1) AS db_journal_papers
        WITH c,j, toFloat(db_journal_papers) / toFloat(total_journal_papers) AS percentage 
        WHERE percentage >= 0.9
        CREATE (j)-[:belongs_to]->(c)
        UNION
        MATCH (co:Conference)--()--(p:Papers) 
        WITH co, count(DISTINCT p) AS total_conference_papers

        MATCH (co)--()--(p2:Papers)--()--(c:Community {name:"Database"})
        WITH c,co, total_conference_papers, count(DISTINCT p2) AS db_conference_papers
        WITH c,co, toFloat(db_conference_papers) / toFloat(total_conference_papers) AS percentage 
        WHERE percentage >= 0.9
        CREATE (co)-[:belongs_to]->(c)
        """,
        #STAGE 3
        """
        MATCH (r:Community {name: "Database"})<-[:belongs_to]-(:Conference|Journal)<-[:belongs_to|belongs_to]-(:Edition|Volume)<-[:published_in|contained_in]-(cited_papers:Papers)<-[citation:cites]-(citing_p:Papers)-[:published_in|contained_in]->(:Edition|Volume)-[:belongs_to|belongs_to]->(:Conference|Journal)-[:belongs_to]->(r)
        WITH r, cited_papers, COUNT(citation) as numcitations
        ORDER BY numcitations DESC
        WITH r, COLLECT(cited_papers)[..100] AS top_cited_papers
        UNWIND top_cited_papers AS paper
        MERGE (paper)-[:is_top_paper_of]->(r)
        """,
        #STAGE 4
        """
        MATCH (a:Author)-[:writes]->(p:Papers)-[:is_top_paper_of]->(r:Community {name: 'Database'})
        WITH r, a, COUNT(p) AS numpapers
        WHERE numpapers >= 2
        MERGE (a)-[:is_a_guru_of]->(r)
        """
    ]
    for i, loading_queries in enumerate(loading_queries, start=1):
        print(f"Executing Query {i}...")
        connection.load_csv_data(loading_queries)

    connection.close()

if __name__ == '__main__':
    main()
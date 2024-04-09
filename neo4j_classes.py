from neo4j import GraphDatabase
from time import time

class Neo4jConnection:

    def __init__(self, uri, user, password):
        self.__uri = uri
        self.__user = user
        self.__password = password
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__password))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def load_csv_data(self, query):
        with self.__driver.session() as session:
            start_time = time()
            result = session.write_transaction(self._execute_query, query)
            execution_time = time() - start_time
            print(f"Query executed in {execution_time:.4f} seconds.")
            return result
        
    def execute_queries_and_print_results(self, queries):
        with self.__driver.session() as session:
            results = session.execute_read(self._execute_queries, queries)
            for result in results:
                print("The query \n{query}\n Returned {records_count} records in {time} ms.\n".format(
                    query=result[1].query, records_count=len(result[0]),
                    time=result[1].result_available_after,
                ))
                for record in result[0]:
                    print(record)
                    print()
        
    @staticmethod
    def _execute_query(tx, query):
        result = tx.run(query)
        return result.single()
    
    @staticmethod
    def _execute_queries(tx, queries):
        results = []
        for query in queries:
            result = tx.run(query)
            records = list(result)
            summary = result.consume()
            results.append((records, summary))
        return results
    
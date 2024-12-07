import sqlite3
import pandas as pd
from typing import List, Dict

class SQLiteTableManager:
    """
    A class to manage SQLite database operations, including creating tables and loading data from CSV files.
    """

    def __init__(self, db_name: str, table_configs: List[Dict[str, any]]):
        """
        Initializes the SQLiteTableManager and processes the table configurations.

        Parameters:
        -----------
        db_name : str
            The name of the SQLite database file.
        table_configs : List[Dict]
            A list of configurations, where each configuration is a dictionary containing:
              - table_name (str): Name of the table.
              - csv_path (str): Path to the CSV file.
              - columns (dict): A dictionary of column names and SQLite data types.
        """
        self.db_name = db_name
        self.table_configs = table_configs
        self._process_tables()

    def _process_tables(self):
        """
        Processes the table configurations by creating tables and loading data from CSV files.
        """
        for config in self.table_configs:
            table_name = config['table_name']
            columns = config['columns']
            csv_path = config['csv_path']
            
            self.create_table(table_name, columns)
            self.insert_from_csv(table_name, csv_path)

    def create_table(self, table_name: str, columns: dict) -> None:
        """
        Creates a table in the SQLite database.

        Parameters:
        -----------
        table_name : str
            The name of the table to be created.
        columns : dict
            A dictionary where keys are column names and values are SQLite data types.
        """
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            columns_definition = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition});")
            conn.commit()

    def insert_from_csv(self, table_name: str, csv_path: str, delimiter: str = ',') -> None:
        """
        Inserts data into a table from a CSV file, avoiding duplication.
    
        Parameters:
        -----------
        table_name : str
            The name of the table where data will be inserted.
        csv_path : str
            The path to the CSV file containing the data.
        delimiter : str, optional
            The delimiter used in the CSV file (default is ',').
        """
        data = pd.read_csv(csv_path, delimiter=delimiter)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]
    
            if row_count == 0:
                data.to_sql(table_name, conn, if_exists='append', index=False)
            else:
                print(f"Data already in {table_name}.")


    def fetch_all(self, table_name: str) -> pd.DataFrame:
        """
        Fetches all data from a table.

        Parameters:
        -----------
        table_name : str
            The name of the table to fetch data from.

        Returns:
        --------
        pd.DataFrame
            A DataFrame containing all the data from the table.
        """
        with sqlite3.connect(self.db_name) as conn:
            query = f"SELECT * FROM {table_name};"
            return pd.read_sql_query(query, conn)

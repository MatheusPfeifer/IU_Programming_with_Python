from code.sqlite_db import SQLiteTableManager
import code.config as config
from code.leastsquare import LeastSquareMatcher
import pandas as pd
from code.exception_handler import exception_handler

@exception_handler
def main():
    # Use the table configurations from config.py
    table_configs = config.table_configs

    # Initialize the SQLiteTableManager with the loaded configurations
    db_manager = SQLiteTableManager("data.db", table_configs)

    # Retrieve the data from the tables to check
    training_data = db_manager.fetch_all("training_data")
    functions_data = db_manager.fetch_all("ideal_functions")
    test_data = db_manager.fetch_all("test_data")

    # Convert fetched data to DataFrames
    df_train = pd.DataFrame(training_data)
    df_ideal = pd.DataFrame(functions_data)
    df_test = pd.DataFrame(test_data)

    # Initialize the LeastSquareMatcher with DataFrames
    matcher = LeastSquareMatcher(df_train, df_test, df_ideal)

    # Find the best least square matches
    matches = matcher.find_best_least_square_matches()
    print("Best Matches:")
    print(matches)

    # Assign the best matching function for test data
    test_results = matcher.assign_best_matching_function(matches)
    print("Test Results with Best Matches:")
    print(test_results)

    # Check for deviations greater than sqrt(2)
    test_results_with_deviation_check = matcher.check_if_deviation_is_greater_than_sqrt2(test_results)
    print("Final Test Results with Deviation Check:")
    print(test_results_with_deviation_check)

if __name__ == "__main__":
    main()

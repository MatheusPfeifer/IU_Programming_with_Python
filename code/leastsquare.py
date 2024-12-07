import pandas as pd
import numpy as np
import math

class LeastSquareMatcher:
    def __init__(self, df_train: pd.DataFrame, df_test: pd.DataFrame, df_functions: pd.DataFrame):
        # Load the datasets
        self.df_train = df_train
        self.df_test = df_test
        self.df_ideal = df_functions

        # Prepare the datasets
        self.dataset1 = self.df_train.copy()
        self.dataset2 = self.df_ideal.copy()

    def find_best_least_square_matches(self) -> pd.DataFrame:
        """
        Finds the best least square matches between two datasets based on the sum of squared residuals.
        
        Returns:
        --------
        pd.DataFrame
            A DataFrame with the best matches and their corresponding least square values and max deviation.
        """
        # Ensure datasets are sorted by 'x'
        self.dataset1 = self.dataset1.sort_values(by='x')
        self.dataset2 = self.dataset2.sort_values(by='x')

        results = []

        # Iterate over columns of dataset1
        for col1 in self.dataset1.columns[1:]:
            best_ls = float('inf')
            best_column = None
            best_max_deviation = None

            # Compare against columns of dataset2
            for col2 in self.dataset2.columns[1:]:
                # Compute Least Square (Sum of Squared Residuals)
                residuals = self.dataset1[col1] - self.dataset2[col2]
                ls = np.sum(residuals ** 2)

                # Compute Maximum Absolute Deviation
                max_deviation = np.max(np.abs(residuals))

                # Update if current LS is smaller
                if ls < best_ls:
                    best_ls = ls
                    best_column = col2
                    best_max_deviation = max_deviation

            # Store results
            results.append({
                'Column_Dataset1': col1,
                'Column_Dataset2': best_column,
                'Least_Square': best_ls,
                'Max_Deviation': best_max_deviation
            })

        # Convert results to DataFrame
        result_df = pd.DataFrame(results)
        return result_df

    def assign_best_matching_function(self, matches: pd.DataFrame) -> pd.DataFrame:
        """
        Assigns the best matching function for each row in the test dataset.
        
        Parameters:
        -----------
        matches : pd.DataFrame
            The DataFrame containing the best matching functions from `find_best_least_square_matches`.
        
        Returns:
        --------
        pd.DataFrame
            The test dataset with the best matching function for each row.
        """
        # Ensure the test dataset and dataset2 are sorted by 'x'
        self.df_test = self.df_test.sort_values(by='x')
        self.dataset2 = self.dataset2.sort_values(by='x')

        # Filter dataset2 to include only rows with x values present in test dataset
        dataset2_filtered = self.dataset2[self.dataset2['x'].isin(self.df_test['x'])]

        # Extract relevant columns from dataset2 based on matches
        relevant_columns = matches['Column_Dataset2'].tolist()
        functions_data = dataset2_filtered[['x'] + relevant_columns]

        # Merge test data with the relevant functions
        merged_data = pd.merge(self.df_test, functions_data, on='x', how='inner')

        # Function to find the best matching function based on absolute deviation
        def find_best_function(row):
            deviations = {col: abs(row['y'] - row[col]) for col in relevant_columns}
            best_function = min(deviations, key=deviations.get)
            best_value = row[best_function]
            deviation = deviations[best_function]
            return best_function, best_value, deviation

        merged_data[['Best_Function', 'Function_Value', 'Deviation']] = merged_data.apply(
            lambda row: pd.Series(find_best_function(row)), axis=1
        )

        # Return the test dataset with additional columns
        return merged_data[['x', 'y', 'Best_Function', 'Function_Value', 'Deviation']]

    def check_if_deviation_is_greater_than_sqrt2(self, test_results: pd.DataFrame, factor=math.sqrt(2)) -> pd.DataFrame:
        """
        Checks if the deviation for each row in the test dataset is greater than sqrt(2).
        
        Parameters:
        -----------
        test_results : pd.DataFrame
            The test dataset with deviations.
        
        Returns:
        --------
        pd.DataFrame
            The test dataset with an additional column indicating whether the deviation is greater than sqrt(2).
        """
        mask = test_results['Deviation'] > factor
        test_results.loc[mask, 'greater_than_sqrt2'] = True
        test_results.loc[~mask, 'greater_than_sqrt2'] = False
        return test_results

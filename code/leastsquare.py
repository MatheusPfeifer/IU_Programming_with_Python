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
        Assigns the best matching function for each row in the test dataset,
        considering the sqrt(2) deviation rule from training. Always returns best match info.

        Parameters:
        -----------
        matches : pd.DataFrame
            DataFrame containing the best matching functions and their max deviations.

        Returns:
        --------
        pd.DataFrame
            The test dataset with best function match, deviation info, and rule compliance.
        """
        self.df_test = self.df_test.sort_values(by='x')
        self.dataset2 = self.dataset2.sort_values(by='x')

        dataset2_filtered = self.dataset2[self.dataset2['x'].isin(self.df_test['x'])]
        relevant_columns = matches['Column_Dataset2'].tolist()
        functions_data = dataset2_filtered[['x'] + relevant_columns]

        merged_data = pd.merge(self.df_test, functions_data, on='x', how='inner')

        deviation_lookup = matches.set_index('Column_Dataset2')['Max_Deviation'].to_dict()

        def evaluate_point(row):
            min_dev = float('inf')
            best_func = None
            best_val = None
            best_dev_train = None
            best_threshold = None
            meets = False

            for col in relevant_columns:
                y_ideal = row[col]
                deviation = abs(row['y'] - y_ideal)
                max_dev_train = deviation_lookup[col]
                threshold = math.sqrt(2) * max_dev_train

                if deviation < min_dev:
                    min_dev = deviation
                    best_func = col
                    best_val = y_ideal
                    best_dev_train = max_dev_train
                    best_threshold = threshold
                    meets = deviation <= threshold  # Atualiza com base no menor

            return best_func, best_val, min_dev, best_dev_train, best_threshold, meets

        merged_data[['Best_Function', 'Function_Value', 'Deviation',
                    'Max_Deviation_Train', 'Deviation_Threshold', 'Meets_Criterion']] = merged_data.apply(
            lambda row: pd.Series(evaluate_point(row)), axis=1
        )

        return merged_data[['x', 'y', 'Best_Function', 'Function_Value', 'Deviation',
                            'Max_Deviation_Train', 'Deviation_Threshold', 'Meets_Criterion']]



import pandas as pd
import unittest

from retrieve_data import clean_dataset


class TestDataTransformation(unittest.TestCase):
    def test_data_transformation(self):
        # Mock file info
        mock_file_info = {
            "important_columns": [
                "area", "date", "year", "life_satisfaction", "mean_salary", "population_size", "number_of_jobs",
                "area_size", "no_of_houses"
            ],
            "column_types": {
                "area": "object", "date": "object", "year": "float64", "life_satisfaction": "float64",
                "mean_salary": "float64", "population_size": "float64", "number_of_jobs": "float64",
                "area_size": "float64", "no_of_houses": "float64"
            }
        }

        # Mock data with errors for testing
        mock_data = pd.DataFrame({
            'area': ['cityoflondon', 'barkinganddagenham', 'barnet', 'bexley', 'brent', 'bromley', 'camden', 'croydon'],
            'date': ['2010-12-01', '2010-12-01', '2013-12-01', '2013-12-01', '2014-12-01', '2014-12-01', '2016-12-01',
                     '2016-12-01'],
            'year': [2010, 2010, 2013, 2013, 2014, 2014, 2016, 2016],
            'life_satisfaction': [7.28, 7.42, 7.28, 7.6, 7.24, 7.01, 7.22, 7.24],
            'median_salary': [33020, 21480, 19568, 18621, 18532, 16720, 23677, 18532],
            'mean_salary': [52203, 24696, 25755, 22580, 23726, 21178, 'nan', 23440],
            'recycling_pct': [0, 3, 8, 18, 6, 13, 13, 13],
            'population_size': [6581, 162444, 313469, 217458, '#', 294902, 190003, 332066],
            'number_of_jobs': [361000, 57000, 138000, 76000, '', 115000, 291000, 160000],
            'area_size': [4323, 15013, 2179, 8650, 5554, 8220, 5044, 1905],
            'no_of_houses': [141300, 120331, 112948, 95406, 87208, 77095, 93638, 80734],
            'borough_flag': [1, 0, 1, 1, 0, 0, 1, 1]
        })

        # Define the expected output
        expected_result = pd.DataFrame({
            'area': ['barnet', 'bexley', 'bromley', 'croydon'],
            'date': ['2013-12-01', '2013-12-01', '2014-12-01', '2016-12-01'],
            'year': [2013.0, 2013.0, 2014.0, 2016.0],
            'life_satisfaction': [7.28, 7.6, 7.01, 7.24],
            'mean_salary': [25755.0, 22580.0, 21178.0, 23440.0],
            'population_size': [313469.0, 217458.0, 294902.0, 332066.0],
            'number_of_jobs': [138000.0, 76000.0, 115000.0, 160000.0],
            'area_size': [2179.0, 8650.0, 8220.0, 1905.0],
            'no_of_houses': [112948.0, 95406.0, 77095.0, 80734.0]
        }).reset_index(drop=True)

        # Call the transformation function
        result = clean_dataset(mock_data, mock_file_info).reset_index(drop=True)

        # Assert that the expected value is returned
        self.assertEqual(True, result.equals(expected_result))


if __name__ == '__main__':
    unittest.main()

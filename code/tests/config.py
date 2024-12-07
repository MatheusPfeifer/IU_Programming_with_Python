# Configurations for code
table_configs = [
    {
        "table_name": "training_data",
        "csv_path": "../data/train.csv",
        "columns": {
            "x": "REAL",
            "y1": "REAL",
            "y2": "REAL",
            "y3": "REAL",
            "y4": "REAL"
        }
    },
    {
        "table_name": "ideal_functions",
        "csv_path": "../data/ideal.csv",
        "columns": {
            "x": "REAL",
            **{f"y{i}": "REAL" for i in range(1, 51)}
        }
    },
    {
    "table_name": "test_data",
    "csv_path": "../data/test.csv",
    "columns": {
        "x": "REAL",
        "y": "REAL",
    }
    }
]
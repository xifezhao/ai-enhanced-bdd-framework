import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import json

class TestPrioritizer:
    """
    Simulates an AI model that prioritizes tests based on historical data.
    """

    def __init__(self, historical_data_path: Path, output_path: Path):
        self.historical_data_path = historical_data_path
        self.output_path = output_path
        self.model = RandomForestClassifier(random_state=42)

    def train_model(self):
        """
        Trains a simple model on historical test data.
        """
        df = pd.read_csv(self.historical_data_path)
        
        # Features: code churn and how many times it failed in the last 10 runs
        X = df[['related_code_churn', 'failures_last_10_runs']]
        # Target: whether it failed in the last run
        y = df['last_run_status'].apply(lambda x: 1 if x == 'fail' else 0)
        
        self.model.fit(X, y)
        print("Test prioritization model trained.")

    def prioritize(self, test_names: list) -> list:
        """
        Predicts the failure probability for a list of tests and sorts them.
        """
        # In a real scenario, you'd fetch current churn/data for these tests.
        # Here, we'll just use the historical data for prediction.
        df = pd.read_csv(self.historical_data_path)
        df = df[df['test_name'].isin(test_names)]

        if df.empty:
            print("Warning: No historical data for the given tests. Returning original order.")
            return test_names
        
        X_predict = df[['related_code_churn', 'failures_last_10_runs']]
        probabilities = self.model.predict_proba(X_predict)[:, 1] # Probability of 'fail'
        
        df['fail_probability'] = probabilities
        
        # Sort by probability, descending
        sorted_df = df.sort_values(by='fail_probability', ascending=False)
        
        prioritized_list = sorted_df['test_name'].tolist()
        
        # Ensure all provided test names are in the output list
        for name in test_names:
            if name not in prioritized_list:
                prioritized_list.append(name)

        print("Tests prioritized based on predicted failure probability.")
        return prioritized_list

    def save_prioritization_order(self, ordered_list: list):
        """Saves the prioritized list to a JSON file."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, 'w') as f:
            json.dump(ordered_list, f, indent=2)
        print(f"Prioritization order saved to {self.output_path}")
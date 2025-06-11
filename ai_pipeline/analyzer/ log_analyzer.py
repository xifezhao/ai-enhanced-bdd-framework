import re
import pandas as pd

class LogAnalyzer:
    """
    Analyzes pytest log files to detect performance anomalies.
    """
    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path

    def parse_log(self) -> pd.DataFrame:
        """
        Parses a pytest log file to extract test names and their execution times.
        """
        # Regex to find '... PASSED [ xx%]' and the duration in parentheses
        log_pattern = re.compile(r"(\S+\.py::\S+)\s+PASSED\s+\[\s*\d+%\s*\]\s+\(.*\)\s+in\s+([\d.]+)")

        test_data = []
        try:
            with open(self.log_file_path, 'r') as f:
                for line in f:
                    # A more robust way to capture duration is from the final report summary
                    # Example line: tests/step_defs/test_login_steps.py::test_successful_login PASSED (0.52s)
                    if "PASSED" in line or "FAILED" in line:
                        parts = line.split()
                        if len(parts) > 2 and parts[1] in ["PASSED", "FAILED"]:
                            test_name = parts[0]
                            # Find duration in parentheses, e.g., (0.52s)
                            duration_match = re.search(r"\((\d+\.\d+)s\)", line)
                            if duration_match:
                                duration = float(duration_match.group(1))
                                test_data.append({"test_name": test_name, "duration": duration})
        except FileNotFoundError:
            print(f"Error: Log file not found at {self.log_file_path}")
            return pd.DataFrame()

        return pd.DataFrame(test_data)

    def detect_anomalies(self):
        """
        Identifies tests with unusually long execution times (outliers).
        """
        df = self.parse_log()
        if df.empty:
            print("No test data found in log file. Cannot perform analysis.")
            return

        mean_duration = df['duration'].mean()
        std_duration = df['duration'].std()
        
        # Anomaly threshold: anything above mean + 2 standard deviations
        threshold = mean_duration + (2 * std_duration)
        
        anomalies = df[df['duration'] > threshold]
        
        print("\n--- Anomaly Detection Report ---")
        if not anomalies.empty:
            print(f"Threshold for performance anomaly: > {threshold:.2f}s")
            for _, row in anomalies.iterrows():
                print(f"[ANOMALY DETECTED] Test '{row['test_name']}' took {row['duration']:.2f}s.")
        else:
            print("No performance anomalies detected.")
        print("------------------------------\n")
import click
from pathlib import Path
import glob

from ai_pipeline.nlp.requirement_parser import RequirementParser
from ai_pipeline.generator.gherkin_generator import GherkinGenerator
from ai_pipeline.prioritizer.test_prioritizer import TestPrioritizer
from ai_pipeline.analyzer.log_analyzer import LogAnalyzer

# Define paths relative to the project root
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
TESTS_DIR = ROOT_DIR / "tests"

@click.group()
def cli():
    """AI-Enhanced BDD Framework CLI"""
    pass

@cli.command()
@click.option('--input-file', required=True, type=click.Path(exists=True), help='Path to the user story text file.')
def generate(input_file):
    """Parses a requirement and generates a Gherkin scenario."""
    click.echo("Starting AI test generation pipeline...")
    
    # Step 1: Parse requirement
    parser = RequirementParser()
    with open(input_file, 'r') as f:
        user_story = f.read()
    parsed_data = parser.parse_user_story(user_story)
    click.echo(f"Parsed requirement: {parsed_data}")

    # Step 2: Generate Gherkin
    generator = GherkinGenerator()
    # Logic to decide which feature file to append to
    feature_file = TESTS_DIR / "features" / "shopping_cart.feature"
    generator.generate_scenario(parsed_data, feature_file)
    
    click.echo("AI test generation pipeline finished.")

@cli.command()
def prioritize():
    """Trains a model and prioritizes existing tests."""
    click.echo("Starting AI test prioritization pipeline...")
    
    historical_data_path = DATA_DIR / "historical_test_data" / "test_results.csv"
    output_path = DATA_DIR / "ai_outputs" / "prioritization_order.json"
    
    prioritizer = TestPrioritizer(historical_data_path, output_path)
    
    # Step 1: Train the model
    prioritizer.train_model()
    
    # Step 2: Get a list of all tests to prioritize
    # A simple way is to get them from the historical data file itself
    import pandas as pd
    all_tests = pd.read_csv(historical_data_path)['test_name'].tolist()
    
    # Step 3: Prioritize and save
    ordered_list = prioritizer.prioritize(all_tests)
    prioritizer.save_prioritization_order(ordered_list)
    
    click.echo(f"Prioritized test order: {ordered_list}")
    click.echo("AI test prioritization pipeline finished.")

@cli.command()
@click.option('--log-file', required=True, type=click.Path(exists=True), help='Path to the pytest log file.')
def analyze(log_file):
    """Analyzes a pytest log file for anomalies."""
    click.echo(f"Starting AI log analysis on {log_file}...")
    
    analyzer = LogAnalyzer(log_file)
    analyzer.detect_anomalies()
    
    click.echo("AI log analysis finished.")

if __name__ == '__main__':
    cli()
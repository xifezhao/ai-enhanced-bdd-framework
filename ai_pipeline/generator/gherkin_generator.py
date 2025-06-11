from pathlib import Path

class GherkinGenerator:
    """
    Generates a Gherkin scenario from structured data and appends it to a feature file.
    """
    
    def generate_scenario(self, parsed_data: dict, feature_file_path: Path):
        """
        Creates a Gherkin scenario string and appends it to the specified .feature file.
        """
        actor = parsed_data.get("actor", "user").replace("_", " ").title()
        main_object = parsed_data.get("object", "item").replace("_", " ")

        # Template for the scenario
        scenario_template = f"""
@needs_review
Scenario: A {actor.lower()} adds a {main_object} to the cart
  Given a registered user is logged in
  And a product "{main_object.title()}" is available
  When the user adds the "{main_object.title()}" to the shopping cart
  Then the shopping cart should contain 1 item of "{main_object.title()}"
"""
        
        try:
            with open(feature_file_path, "a") as f:
                f.write("\n" + scenario_template)
            print(f"Successfully appended AI-generated scenario to {feature_file_path}")
        except FileNotFoundError:
            print(f"Error: Feature file not found at {feature_file_path}")
            
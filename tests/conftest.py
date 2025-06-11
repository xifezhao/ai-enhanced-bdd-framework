import pytest
from selenium import webdriver
from pathlib import Path
import json

# Define project root to find data files
ROOT_DIR = Path(__file__).parent.parent
AI_OUTPUTS_DIR = ROOT_DIR / "data" / "ai_outputs"

# --- Command Line Options ---
def pytest_addoption(parser):
    """Adds custom command-line options to pytest."""
    parser.addoption(
        "--prioritize", action="store_true", default=False, help="Enable AI test prioritization"
    )

# --- Fixtures ---
@pytest.fixture(scope="session")
def browser():
    """Manages the Selenium WebDriver instance."""
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Uncomment for CI environments
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# --- Hooks ---
def pytest_collection_modifyitems(config, items):
    """
    This hook is called after test collection. It reorders tests if --prioritize is used.
    """
    if not config.getoption("--prioritize"):
        return

    print("\nAI Prioritization enabled. Reordering tests...")
    
    order_file = AI_OUTPUTS_DIR / "prioritization_order.json"
    if not order_file.exists():
        print("Warning: prioritization_order.json not found. Running tests in default order.")
        return

    with open(order_file, 'r') as f:
        prioritized_order = json.load(f)

    # Create a mapping of test name to its priority index
    # We use a simple name matching logic here. A more robust solution might use custom markers.
    test_map = {item.name: item for item in items}
    priority_map = {name: i for i, name in enumerate(prioritized_order)}
    
    # Simple name mapping from historical data to pytest node name
    def map_historical_name_to_pytest_name(historical_name):
        # e.g., 'test_successful_login' -> 'test_successful_login'
        # e.g., 'test_add_item_to_cart' -> 'test_add_an_item_to_the_cart' (pytest-bdd generated name)
        # This is tricky and a major challenge. We'll use a simple direct mapping for the PoC.
        # In a real project, you would need a more robust mapping strategy.
        for pytest_name in test_map:
            if historical_name in pytest_name:
                return pytest_name
        return None

    sorted_items = []
    processed_pytest_names = set()

    for historical_name in prioritized_order:
        pytest_name = map_historical_name_to_pytest_name(historical_name)
        if pytest_name and pytest_name in test_map and pytest_name not in processed_pytest_names:
            sorted_items.append(test_map[pytest_name])
            processed_pytest_names.add(pytest_name)

    # Add any remaining tests that were not in the priority list
    for item in items:
        if item.name not in processed_pytest_names:
            sorted_items.append(item)
    
    items[:] = sorted_items
    
    print("Test execution order after prioritization:")
    for i, item in enumerate(items):
        print(f"  {i+1}. {item.name}")
    print("-" * 30)
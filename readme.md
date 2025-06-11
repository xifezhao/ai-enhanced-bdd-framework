# AI-Enhanced BDD Framework (PyTest-BDD)

![CI Pipeline](https://github.com/your-username/ai-enhanced-bdd-framework/actions/workflows/ci.yml/badge.svg)

This project is a Proof-of-Concept (PoC) demonstrating how to integrate Artificial Intelligence (AI) and automation into a Behavior-Driven Development (BDD) testing workflow. It serves as the official, executable case study for the academic paper:

> **Zhao, X., Wang, H., Ding, J., Hu, Z., Tian, Q., & Wang, Y. (Year). *Augmenting Software Quality Assurance with AI and Automation using PyTest-BDD*. Journal Name, Volume(Issue), pages.**

We use a simulated e-commerce web application as the Application Under Test (AUT) to showcase an end-to-end process, from parsing natural language requirements to automated test execution and intelligent, AI-driven analysis.

## Core Concepts Demonstrated

This framework implements several key concepts from the paper:

1.  **AI Requirement Analysis & Test Generation**: Automatically converts natural language user stories into syntactically correct Gherkin `.feature` files using Natural Language Processing (NLP).
2.  **Human-in-the-Loop (HIL) Feedback Mechanism**: AI-generated scenarios are explicitly tagged for human review (`@needs_review`), ensuring a collaborative and quality-controlled process.
3.  **AI Test Case Prioritization**: Before execution, a machine learning model, trained on historical data, prioritizes test cases to run high-risk and high-impact scenarios first, enabling faster feedback.
4.  **Automated Test Execution**: End-to-end web tests are executed using the robust `pytest-bdd` framework, integrated with `Selenium` for browser automation.
5.  **AI Anomaly Detection & Reporting**: Post-execution, test logs and performance metrics are analyzed to automatically identify potential performance bottlenecks or other unexpected behaviors that traditional pass/fail assertions might miss.
6.  **CI/CD Integration**: A sample GitHub Actions workflow (`.github/workflows/ci.yml`) is provided to demonstrate how to automate the entire AI-enhanced testing pipeline.

---

## Installation & Setup

Follow these steps to get the project running on your local machine.

### Prerequisites

*   Python 3.9+
*   Google Chrome browser installed

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-enhanced-bdd-framework.git
cd ai-enhanced-bdd-framework
```

### 2. Create and Activate a Virtual Environment
This isolates the project dependencies from your global Python environment.

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download NLP Models
The framework uses SpaCy for NLP tasks. This command downloads the required English model.
```bash
python -m spacy download en_core_web_sm
```

### 5. WebDriver Setup
The project uses `selenium`. Recent versions of Selenium include **Selenium Manager**, which should automatically download the correct `chromedriver` for your installed version of Google Chrome. If you encounter issues, you may need to manually install `chromedriver` and ensure it's in your system's `PATH`.

---

## How to Run the End-to-End Workflow

This step-by-step guide walks you through the entire AI-enhanced testing lifecycle as described in the paper.

### Step 0: Start the Application Under Test (AUT)

Open a terminal and run the Flask web application. This server must remain running in the background for the tests.
```bash
flask --app src.app run
```
You can access the application at `http://127.0.0.1:5000`.

### Step 1: AI-Powered Test Scenario Generation

In a **new terminal** (while the app is running), execute the AI pipeline to parse a user story and generate a corresponding Gherkin scenario.

```bash
python ai_pipeline/main_pipeline.py generate --input-file data/requirements_input/user_story_01.txt
```

**Expected Outcome:** A new scenario, tagged with `@needs_review`, will be appended to the `tests/features/shopping_cart.feature` file.

### Step 2: Human-in-the-Loop Review

This is a manual step representing the essential collaboration between AI and a human tester.

1.  Open `tests/features/shopping_cart.feature` in your code editor.
2.  Review the newly added scenario.
3.  If you approve of its content and structure, **delete the `@needs_review` tag**. This action signals that the test is validated and ready for execution.

### Step 3: Run Tests with AI Prioritization

First, let the AI model analyze historical data to determine the optimal test order.

```bash
python ai_pipeline/main_pipeline.py prioritize
```
This creates a `prioritization_order.json` file in `data/ai_outputs/`.

Next, run `pytest` using the custom `--prioritize` flag. This flag activates a hook in `conftest.py` that reorders the tests according to the AI's recommendation.

```bash
pytest --prioritize -v
```

**Observe the output:** The tests will not run in the default alphabetical order. Instead, tests predicted as more likely to fail (e.g., `test_performance_of_product_page`, `test_add_item_to_cart`) will run first.

### Step 4: AI-Powered Anomaly Detection

To perform post-execution analysis, first run the tests and generate a detailed log file.

```bash
pytest --log-cli-level=INFO --log-file=pytest.log
```
*Note: We run without `--prioritize` here to get a baseline log, but it works with it as well.*

Now, run the AI analysis script on the generated log.

```bash
python ai_pipeline/main_pipeline.py analyze --log-file pytest.log
```
**Expected Outcome:** The script will analyze the execution times of all tests. If a test's duration is a statistical outlier (e.g., the product page test, which is designed to be slow intermittently), the console will print an anomaly report.

```
--- Anomaly Detection Report ---
Threshold for performance anomaly: > 1.25s
[ANOMALY DETECTED] Test 'tests/step_defs/test_shopping_cart.py::test_add_an_item_to_the_cart' took 2.85s.
------------------------------
```

---

## Project Structure Explained

-   `.github/workflows/`: Contains the CI pipeline configuration for GitHub Actions.
-   `ai_pipeline/`: The core AI logic, separated into modules for parsing, generation, prioritization, and analysis.
-   `data/`: Holds all data used by the AI pipeline, including input requirements, historical test data for training, and AI-generated outputs.
-   `src/`: The simple Flask e-commerce application that serves as the AUT.
-   `tests/`: All `pytest-bdd` test code.
    -   `features/`: Human-readable `.feature` files written in Gherkin.
    -   `step_defs/`: Python files that implement the Gherkin steps using Selenium.
    -   `conftest.py`: The central pytest configuration file, containing fixtures (like the browser setup) and hooks (for prioritization).

## Limitations of this PoC

This project is a conceptual demonstration and has several simplifications:

-   **NLP Model**: The requirement parser uses simple rule-based logic. A production system would require a more sophisticated, fine-tuned NLP model.
-   **Gherkin Generation**: The generator uses a fixed template. Advanced systems might use generative models (like GPT) to create more varied and complex scenarios.
-   **Prioritization Model**: The model is trained on a small, static CSV file. A real-world MLOps pipeline would continuously retrain this model on live data from CI/CD runs and code repository metrics.
-   **Test Name Mapping**: The mapping between historical test names and pytest's internal node names in `conftest.py` is a known challenge. This PoC uses a simple substring match, but a robust solution might involve custom pytest markers.

<!-- ## Citing this Work

  If you use this framework or concepts from this repository in your research, please cite our paper:

```bibtex
@article{zhao2024augmenting,
  title={Augmenting Software Quality Assurance with AI and Automation using PyTest-BDD},
  author={Zhao, Xiaofei and Wang, Hua and Ding, JieQiong and Hu, Zhiming and Tian, Qingqing and Wang, Ying},
  journal={Journal of Software Engineering and Applications},
  year={2024},
  publisher={Example Publisher}
}
```
 -->
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
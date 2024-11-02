# JSON Path Experiment

This experiment is a JSON path-finding task designed to test participants' ability to identify correct JSON object paths. The interface presents randomly generated JSON structures with various depths and fields. Participants are tasked with locating a specific target attribute path in each JSON structure. The JSON object can appear in either an indented or non-indented format.

## Features
- **Path Construction by Button**: Participants can build the path incrementally by selecting JSON keys displayed as buttons.
- **Direct Path Entry**: Alternatively, the target path can be entered directly in a text field for faster submission.
- **Feedback and Attempts Tracking**: Each attempt is evaluated, with feedback on whether the path is correct or incorrect, and the number of attempts is tracked.
- **Time Tracking and Progression**: The experiment includes 30 questions, with an equal distribution of indented and non-indented JSON structures, and records the time taken for each question.

## Installation

### Requirements
- Python 3.7 or higher

### Installation Instructions

1. **Clone or Download the Repository**
   ```bash
   git clone git@github.com:N777W/BP-Indentation-JSON.git
   cd BP-Indentation-JSON   ```

2. **Set Up Environment**
   - (Optional) Create a virtual environment to manage dependencies:
     ```bash
     python -m venv json_experiment_env
     source json_experiment_env/bin/activate  # On Windows: json_experiment_env\Scripts\activate
     ```

3. **Install Dependencies**
   - Install dependencies from the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Script**
   ```bash
   python main.py
   ```

## How to Use the Experiment

1. **Starting the Experiment**:
   - The program starts with a JSON object displayed on the screen.
   - A target attribute (i.e., the JSON path to locate) is provided at the top of the interface.

2. **Path Construction**:
   - **Button Selection**: The keys of the JSON object are displayed as buttons. Click each button to build the path step-by-step. The selected path is displayed in the input field.
   - **Direct Entry**: Alternatively, type the entire path in the provided text entry box and press "Submit" or Enter.

3. **Submission and Feedback**:
   - After constructing the path, press "Submit Path" or the Enter key to verify it.
   - Feedback will display whether the path is correct or incorrect. If correct, you will proceed to the next question; otherwise, you can try again.

4. **Experiment Completion and Data Saving**:
   - After 30 questions, the experiment completes, and the results, including time and attempt data for each question, are saved to `JSONPathExperimentResults.xlsx`.

## Experiment Structure

Each JSON structure is generated with a random layout, following these specifications:
- **JSON Depth**: Up to 3 nested levels to ensure readability.
- **Indented/Non-Indented**: Randomized format, with an equal distribution of 15 indented and 15 non-indented JSONs per experiment.

## Data and Analysis

At the end of the experiment, the results are saved in `JSONPathExperimentResults.xlsx`, which contains:
- **Question**: The question number.
- **Correct Path**: The correct JSON path.
- **User Path**: The path provided by the user.
- **Attempts**: The number of attempts made before finding the correct path.
- **Time Taken (s)**: The time taken to complete each question.


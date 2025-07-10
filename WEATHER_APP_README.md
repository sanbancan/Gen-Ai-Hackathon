# Weather Insight Generator

A Flask web application that integrates with OpenAI's API to provide weather insights based on city mentions in conversations. The application demonstrates fine-tuning an AI model with weather data and generating contextual insights.

## Features

- Preprocesses weather data from a mock Kaggle dataset
- Fine-tunes an OpenAI GPT-3.5 model with custom weather insights
- Provides a web interface to view generated insights
- Processes conversation transcriptions to extract city names and relevant weather information

## Prerequisites

- Python 3.7+
- OpenAI API key
- Required Python packages (install via `pip install -r requirements.txt`):
  - flask
  - openai
  - pandas

## Installation

1. Install the required packages:
   ```bash
   pip install flask openai pandas
   ```

2. Set up your OpenAI API key:
   - Replace the `OPENAI_API_KEY` in `all.py` with your actual OpenAI API key
   - Or set it as an environment variable before running the application

## Usage

1. Run the application:
   ```bash
   python all.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. The application will display a sample conversation transcription and its corresponding weather insight.

## How It Works

1. **Data Preprocessing**: 
   - The application creates a mock dataset with weather information for different cities.
   - It generates prompt-completion pairs for fine-tuning the AI model.

2. **Model Fine-tuning**:
   - Uploads the training data to OpenAI.
   - Initiates fine-tuning of the GPT-3.5 model with the custom dataset.
   
3. **Web Interface**:
   - Provides a simple web interface to view the generated insights.
   - Displays the original transcription and the AI-generated weather insight.

## File Structure

- `all.py`: Main application file containing the Flask app, data processing, and model integration.
- `test_app.py`: A simple test Flask application (can be used for basic testing).
- `templates/`: Directory containing HTML templates for the web interface.
  - `index.html`: Main template for displaying insights.

## Notes

- The fine-tuning process may take 10-30 minutes to complete.
- The application uses a mock dataset. For production use, replace it with real weather data.
- Ensure you have sufficient API credits with OpenAI for fine-tuning and inference.

## License

This project is open source and available under the MIT License.

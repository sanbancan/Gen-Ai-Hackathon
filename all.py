# cook your dish here
import pandas as pd
import json
import os
from openai import OpenAI
from flask import Flask, render_template
import threading

# Initialize Flask app
app = Flask(__name__)

# Open AI API key (replace with your key)
OPENAI_API_KEY = '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'  # Set in IDE environment or replace here
client = OpenAI(api_key=OPENAI_API_KEY)

# Step 1: Preprocess Kaggle dataset
def preprocess_data():
    # Mock Kaggle dataset (replace with actual CSV from Kaggle)
    data = {
        'city': ['Seattle', 'Chicago', 'New York'] * 34,  # ~100 rows
        'temperature': [15.5, 20.0, 18.0] * 34,
        'precipitation': [10.0, 5.0, 2.0] * 34
    }
    df = pd.DataFrame(data).head(100)

    # Create prompt-completion pairs for fine-tuning
    fine_tune_data = []
    for _, row in df.iterrows():
        prompt = f"Conversation mentions {row['city']}. Provide a weather insight."
        completion = f"In {row['city']}, expect {row['temperature']}°C and {row['precipitation']}mm rain. Plan accordingly."
        fine_tune_data.append({"prompt": prompt, "completion": completion})

    # Save to JSONL
    with open('fine_tune_data.jsonl', 'w') as f:
        for entry in fine_tune_data:
            f.write(json.dumps(entry) + '\n')
    return 'fine_tune_data.jsonl'

# Step 2: Fine-tune Open AI model
def fine_tune_model():
    try:
        # Upload file
        with open('fine_tune_data.jsonl', 'rb') as f:
            file_response = client.files.create(file=f, purpose='fine-tune')
        
        # Start fine-tuning
        fine_tune_response = client.fine_tuning.jobs.create(
            training_file=file_response.id,
            model='gpt-3.5-turbo'
        )
        print(f"Fine-tuning started: {fine_tune_response.id}")
        return fine_tune_response.id  # Note: Fine-tuning takes ~10-30 min
    except Exception as e:
        print(f"Fine-tuning error: {e}")
        return None

# Step 3: Generate insight from mock transcription
def generate_insight(transcription, model_id='gpt-3.5-turbo'):  # Default model if fine-tuning incomplete
    try:
        # Extract city (simple keyword match)
        cities = ['Seattle', 'Chicago', 'New York']
        city = next((c for c in cities if c.lower() in transcription.lower()), 'Unknown')
        
        # Call Open AI model
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": f"Conversation mentions {city}. Provide a weather insight."}],
            max_tokens=50
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating insight: {e}"

# Step 4: Flask UI
@app.route('/')
def display_insights():
    # Mock transcription
    transcription = "Planning reforestation in Seattle next week"
    insight = generate_insight(transcription)  # Replace model_id with fine-tuned ID when ready
    return render_template('index.html', insight=insight, transcription=transcription)

# HTML template as a string (since online IDE may not support separate files)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<body>
    <h1>Live Call Insights</h1>
    <p><b>Transcription:</b> {{ transcription }}</p>
    <p><b>Insight:</b> {{ insight }}</p>
</body>
</html>
"""

# Step 5: Main execution
def main():
    # Create templates folder and index.html
    os.makedirs('templates', exist_ok=True)
    with open('templates/index.html', 'w') as f:
        f.write(HTML_TEMPLATE)
    
    # Preprocess data
    preprocess_data()
    
    # Start fine-tuning (comment out if already done and use fine-tuned model ID)
    fine_tune_id = fine_tune_model()
    print("Note: Fine-tuning may take 10-30 minutes. Use model_id='ft:gpt-3.5-turbo:your-org:custom-id' in generate_insight() once complete.")
    
    # Run Flask app in a separate thread
    print("Starting Flask app at http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)

# Run the app
if __name__ == '__main__':
    threading.Thread(target=main).start()
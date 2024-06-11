import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv
load_dotenv()


api_key = os.getenv('OPENAI_API_KEY')
chrome_extention_id = os.getenv('CHROME_EXTENTION_ID')

app = Flask(__name__)
CORS(app, resources={r"/api/generate-url-YsQ8azA4": {"origins": chrome_extention_id}})

client = openai.OpenAI(
    api_key=api_key,
    # base_url="https://api.openai.iniad.org/api/v1", # INIAD AI-MOP
)

@app.route('/api/generate-url-YsQ8azA4', methods=['POST'])
def generate_calendar_url():
    data = request.json
    text = data.get('text')
    prompt = f'This year is 2024.\n{text}\nCreate a Google Calendar URL from the previous text.\nYou should only respond in the format as described below:\nRESPONSE FORMAT:\nhttps://calendar.google.com/calendar/r/eventedit?..."'
    
    try:
        # Create text for LLM
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': 'user', 'content': prompt},
        ]
        )
        ans = response.choices[0].message.content

        # Regular expression
        match = re.search(r'https://[^\s]+', ans)
        if match: url = match.group()

        return jsonify({'url': url})
    except Exception as e:
        print('Error generating URL:', e)
        return jsonify({'error': 'Error generating URL'}), 500

if __name__ == '__main__':
    app.run(debug=True)

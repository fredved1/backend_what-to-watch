# What to Watch - Movie Recommendation Assistant

An intelligent movie and TV show recommendation system that helps users discover content across various streaming platforms. The assistant uses GPT-4 to provide personalized recommendations based on user preferences and available streaming services.

## Features

- Personalized movie and TV show recommendations
- Support for multiple streaming platforms (Netflix, Prime Video, Disney+, etc.)
- Direct links to watch content on your preferred platform
- Focus on discovering hidden gems and underrated titles
- Clean and intuitive Streamlit interface

## Tech Stack

- Backend: Flask + LangChain + OpenAI GPT-4
- Frontend: Streamlit
- Deployment: Heroku

## Setup

1. Clone the repository:
```bash
git clone https://github.com/[your-username]/backend_what-to-watch.git
cd backend_what-to-watch
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

5. Start the Flask backend:
```bash
python app.py
```

6. In a new terminal, start the Streamlit frontend:
```bash
streamlit run streamlit_app.py
```

7. Open your browser and navigate to `http://localhost:8501`

## Usage

1. Select your available streaming platforms from the list
2. Share your viewing preferences (genres, favorite shows, mood, etc.)
3. Receive personalized recommendations with direct links to watch
4. Ask for more recommendations or refine your preferences

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
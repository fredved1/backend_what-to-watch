# What To Watch - Movie Recommendation Backend

A Flask-based backend for the "What To Watch" movie recommendation app. This backend uses OpenAI's GPT models to generate personalized movie recommendations and enhances them with movie details and posters from TMDB.

## Features

- AI-powered movie recommendations using OpenAI's GPT models
- Integration with TMDB for movie details and posters
- RESTful API endpoints for recommendations
- Deployed on Azure App Service

## API Endpoints

- `GET /` - Home endpoint with service information
- `GET /health` - Health check endpoint
- `GET /test` - Test endpoint
- `POST /recommend` - Get movie recommendations based on user input
- `POST /api/send-message` - Send a message to the AI and get a response
- `POST /api/start-conversation` - Start a new conversation
- `POST /api/clear-memory` - Clear the conversation memory

## Tech Stack

- Flask: Web framework
- LangChain: For building LLM applications
- OpenAI: For generating recommendations
- TMDB API: For movie details and posters
- Azure: For deployment

## Local Development

1. Clone the repository
```bash
git clone https://github.com/fredved1/backend_what-to-watch.git
cd backend_what-to-watch
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys
```
OPENAI_API_KEY=your_openai_api_key
TMDB_API_KEY=your_tmdb_api_key
```

5. Run the Flask app
```bash
python app.py
```

## Deployment

This backend is deployed on Azure App Service. The deployment is automated using GitHub Actions.

## Frontend

The frontend for this app is a Next.js application that can be found in a separate repository.

## License

MIT 
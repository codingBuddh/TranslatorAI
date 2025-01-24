# TranslatorAI
A Text-based System that is language neutral, powered by OpenAI's API and built with FastAPI and React.

## Project Overview
TranslatorAI is a multilingual text translation software that leverages OpenAI's API for accurate translations. The system features a FastAPI backend, React frontend, and integrates LangChain and LangSmith for prompt visualization and tracing.

## Setup

### Backend Setup

1. Create a Python virtual environment:
```bash
python -m venv TranslatorEnv
```

2. Activate the virtual environment:
- Windows:
```bash
TranslatorEnv\Scripts\activate
```
- macOS/Linux:
```bash
source TranslatorEnv/bin/activate
```

3. Install required packages:
```bash
pip install fastapi uvicorn python-dotenv langchain openai
```

### Frontend Setup
(Coming soon)

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── public/
└── README.md
```

## Features
- Multi-language text translation
- Real-time translation using OpenAI's API
- Prompt visualization with LangChain
- Translation history tracking
- Clean, futuristic UI

## Development
Once your environment is activated, you'll see `(TranslatorEnv)` at the beginning of your terminal prompt.

## Contributing
Please read our contributing guidelines before submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

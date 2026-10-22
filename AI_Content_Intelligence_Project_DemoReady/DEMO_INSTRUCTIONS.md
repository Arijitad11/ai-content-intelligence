# Demo-ready version

## Run without API credits

```powershell
streamlit run app.py
```

The app works in Demo Mode even when the OpenAI API has no credits. Generate a strategy, load the demo pipeline, then show Performance Analytics and AI Insights.

## Use OpenAI later

If you add API credits:

```powershell
$env:OPENAI_API_KEY="YOUR_REAL_KEY"
streamlit run app.py
```

The app will try the API. If billing, authentication, network or other API problems occur, it automatically falls back to Demo Mode instead of crashing.

## Security

Never put your API key in `app.py`, screenshots, README files or GitHub.

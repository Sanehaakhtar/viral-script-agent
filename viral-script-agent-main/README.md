# Hosted application
https://viralgen-saneha.streamlit.app/

# Viral Script Agent (viralgen)

A Streamlit app that generates short-form viral video scripts using:

- Groq LLM (`llama-3.3-70b-versatile`) for script writing and scoring
- Tavily search for trend/fact grounding
- Platform and persona presets for social content optimization

The app is designed for rapid idea-to-script generation for short video platforms like TikTok, Reels, and Shorts.

## Features

- Customizable generation inputs:
  - Topic
  - Platform (TikTok, Instagram Reels, YouTube Shorts, Snapchat Spotlight)
  - Script duration (15s/30s/60s/90s)
  - Persona/tone
  - Visual style
  - Slang density and selected slang terms
  - Music vibe
  - Hashtag count
- Trend-informed script creation:
  - Pulls fresh topical info via Tavily search
  - Summarizes findings and injects them into generation prompt
- Auto-generated output package:
  - Structured script (hook/body/call-to-action style prompt guidance)
  - Aura score (1-1000)
  - Estimated views and engagement (simulated)
  - Suggested hashtag set
- Streamlit UI with a fully customized red/black visual theme

## Tech Stack

- Python
- Streamlit
- LangChain + Groq integration (`langchain_groq`)
- Tavily search tool (`langchain_community.tools.tavily_search`)

## Project Structure

```text
viral-script-agent-main/
  requirements.txt
  viral-gen.py
  .devcontainer/
    devcontainer.json
```

## Requirements

From `requirements.txt`:

- `streamlit`
- `crewai`
- `langchain_groq`
- `langchain_community`

## Prerequisites

You need API keys for:

- Groq (`GROQ_API_KEY`)
- Tavily (`TAVILY_API_KEY`)

The app expects these in Streamlit secrets.

## Local Setup

1. Clone the repository and open the project folder.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Add your Streamlit secrets.
5. Run the app.

Example commands (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "your_groq_api_key"
TAVILY_API_KEY = "your_tavily_api_key"
```

Start Streamlit:

```powershell
streamlit run viral-gen.py
```

## Usage

1. Open the app in your browser (Streamlit will print the local URL).
2. Select generation settings in the sidebar.
3. Enter a topic (for example: "ai side hustles" or "sleep optimization").
4. Click **generate viral script**.
5. Copy script and hashtags from the output text areas.

## How It Works

1. The app validates that required API keys are available in Streamlit secrets.
2. On generation:
   - Tavily fetches recent trend/fact results for your topic.
   - Groq summarizes this research into compact viral facts.
   - Groq generates the final script with your selected style parameters.
   - A second Groq call estimates an "aura score" from 1-1000.
3. The UI displays script, score, estimated metrics, and hashtags.

## Notes and Limitations

- Estimated views and engagement are randomized placeholders, not predictive analytics.
- Output quality depends heavily on topic specificity and API responsiveness.
- If secrets are missing, the app will show an error and stop generation.

## Troubleshooting

- Error: "api keys not found in secrets"
  - Ensure `.streamlit/secrets.toml` exists and keys are correctly named.
- Tavily/Groq request failures
  - Verify API keys, quota, and internet connectivity.
- Dependency errors
  - Re-run `pip install -r requirements.txt` inside the active virtual environment.

## Deployment

### Streamlit Community Cloud

1. Push this repo to GitHub.
2. Create a new Streamlit app and point it to `viral-gen.py`.
3. Add `GROQ_API_KEY` and `TAVILY_API_KEY` in Streamlit app secrets.
4. Deploy.

Live app:
https://viralgen-saneha.streamlit.app/

## Security

- Never hardcode API keys in source code.
- Use Streamlit secrets or environment-managed secrets in deployment.

## License

Add a license file if you plan to distribute this project publicly.
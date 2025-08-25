import os, json, subprocess, requests

GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
GITHUB_EVENT_PATH = os.environ["GITHUB_EVENT_PATH"]
PR_NUMBER = json.load(open(GITHUB_EVENT_PATH))["number"]

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

diff = subprocess.check_output(["git", "diff", "origin/main...HEAD"]).decode()

prompt = f"Review this code diff and suggest improvements:\n\n{diff}"

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
headers = {"Content-Type": "application/json"}
params = {"key": GEMINI_API_KEY}
payload = {"contents": [{"parts": [{"text": prompt}]}]}

r = requests.post(url, headers=headers, params=params, json=payload)
r.raise_for_status()
data = r.json()
review_text = data["candidates"][0]["content"]["parts"][0]["text"]

api_url = f"https://api.github.com/repos/{GITHUB_REPOSITORY}/issues/{PR_NUMBER}/comments"
headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
requests.post(api_url, headers=headers, json={"body": f"🤖 AI Review:\n\n{review_text}"})

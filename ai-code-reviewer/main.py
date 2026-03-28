import os
import httpx # type: ignore
from dotenv import load_dotenv # type: ignore
from fastapi import FastAPI, Request # type: ignore
from fastapi.middleware.trustedhost import TrustedHostMiddleware # type: ignore
from llm_client import get_code_review

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*.ngrok-free.app", "localhost"]
)

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/webhook/github")
async def handle_webhook(request: Request):
    payload = await request.json()

    action = payload.get("action")

    if not action:
        return {"message": "No action found in payload"}
    
    if action not in ["opened", "synchronize"]:
        return {"message": "Action is ignored"}
    
    repo_full_name = payload["repository"]["full_name"]
    pr_number = payload["pull_request"]["number"]
    api_url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"

    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3.diff",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        response = await client.get(api_url, headers=headers)
        diff_text = response.text
    
    review_data = get_code_review(diff_text)

    comment_body = f"AI Code Review: \n{review_data.summary}\n"

    if review_data.critical_bugs:
        comment_body += "\nPotential critical bugs detected!\n"

    comment_body += "AI Suggestions:" + "\n".join([f"- {s}" for s in review_data.suggestions])

    comment_url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"

    async with httpx.AsyncClient() as client:
        await client.post(
            comment_url,
            json={"body": comment_body},
            headers={"Authorization": f"token {GITHUB_TOKEN}"}
        )


    return {"status": "success", "review_posted": True}


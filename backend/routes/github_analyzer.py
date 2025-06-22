import requests
from flask import Blueprint, request, jsonify
import re
import os
import random
import google.generativeai as genai

GITHUB_TOKEN = "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"
GITHUB_API_URL = "https://api.github.com"
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

analyzer_bp = Blueprint('github_analyzer', __name__)

def extract_owner_repo(url):
    # Accepts URLs like https://github.com/owner/repo or git@github.com:owner/repo.git
    m = re.match(r"https?://github.com/([^/]+)/([^/]+?)(?:.git)?/?$", url)
    if m:
        return m.group(1), m.group(2)
    m = re.match(r"git@github.com:([^/]+)/([^/]+?)(?:.git)?$", url)
    if m:
        return m.group(1), m.group(2)
    return None, None

def get_github_api_key():
    keys = os.getenv("GITHUB_API_KEYS", "").split(",")
    keys = [k.strip() for k in keys if k.strip()]
    # Fallback to the new provided key if none are configured
    if not keys:
        return "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"
    return random.choice(keys)

def get_openrouter_api_key():
    # Always use the provided OpenRouter API key
    return "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"

def get_gemini_api_key():
    # In a real app, use os.getenv("GEMINI_API_KEY", "your_fallback_key")
    return "AIzaSyC4j5ZnPh9rUpkILuEgG1OdC-8TB96Qr5I"

@analyzer_bp.route('/github-analyze', methods=['POST'])
def github_analyze():
    data = request.get_json()
    repo_url = data.get('repo_url')
    if not repo_url:
        return jsonify({'error': 'Missing repo_url'}), 400
    owner, repo = extract_owner_repo(repo_url)
    if not owner or not repo:
        return jsonify({'error': 'Invalid GitHub repo URL'}), 400
    
    headers = {
        'Authorization': f'token {get_github_api_key()}',
        'Accept': 'application/vnd.github+json'
    }
    
    # Get real open issues count (excluding PRs)
    search_issues_url = f"{GITHUB_API_URL}/search/issues?q=repo:{owner}/{repo}+is:issue+is:open"
    search_issues_resp = requests.get(search_issues_url, headers=headers)
    if search_issues_resp.status_code != 200:
        return jsonify({'error': 'Failed to fetch real open issues count.', 'details': search_issues_resp.text}), 400
    total_issues = search_issues_resp.json().get('total_count', 0)

    # Get top 10 contributors for display
    contrib_list_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contributors"
    contrib_list_resp = requests.get(contrib_list_url, headers=headers)
    if contrib_list_resp.status_code != 200:
        return jsonify({'error': 'Failed to fetch contributors list', 'details': contrib_list_resp.text}), 400
    contributors = contrib_list_resp.json()[:10]

    # Get total contributor count accurately and efficiently
    count_contrib_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contributors?per_page=1"
    count_contrib_resp = requests.get(count_contrib_url, headers=headers)
    
    total_contributors = 0
    if count_contrib_resp.status_code == 200:
        if 'Link' in count_contrib_resp.headers:
            link_header = count_contrib_resp.headers['Link']
            match = re.search(r'page=(\d+)>; rel="last"', link_header)
            if match:
                total_contributors = int(match.group(1))
            else: 
                total_contributors = len(contrib_list_resp.json()) if contrib_list_resp.json() is not None else 0
        else:
            total_contributors = len(contrib_list_resp.json()) if contrib_list_resp.json() is not None else 0
    else:
        total_contributors = -1 # Indicates an error in fetching the count

    result = []
    for c in contributors:
        login = c['login']
        avatar_url = c['avatar_url']
        # Get latest commit by this contributor
        commits_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits?author={login}&per_page=2"
        commit_resp = requests.get(commits_url, headers=headers)
        recent_commits = []
        if commit_resp.status_code == 200 and commit_resp.json():
            for commit in commit_resp.json():
                recent_commits.append({
                    'message': commit['commit']['message'],
                    'url': commit['html_url'],
                    'date': commit['commit']['author']['date']
                })
        result.append({
            'login': login,
            'avatar_url': avatar_url,
            'contributions': c.get('contributions', 0),
            'recent_commits': recent_commits
        })
    return jsonify({
        'total_issues': total_issues,
        'total_contributors': total_contributors,
        'contributors': result
    })

@analyzer_bp.route('/github-generate-issues', methods=['POST'])
def github_generate_issues():
    data = request.get_json()
    repo_url = data.get('repo_url')
    if not repo_url:
        return jsonify({'error': 'Missing repo_url'}), 400
    owner, repo = extract_owner_repo(repo_url)
    if not owner or not repo:
        return jsonify({'error': 'Invalid GitHub repo URL'}), 400
    
    headers = {
        'Authorization': f'token {get_github_api_key()}',
        'Accept': 'application/vnd.github+json'
    }
    # Get contributors
    contrib_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contributors"
    contrib_resp = requests.get(contrib_url, headers=headers)
    if contrib_resp.status_code != 200:
        return jsonify({'error': 'Failed to fetch contributors', 'details': contrib_resp.text}), 400
    contributors = contrib_resp.json()[:10]
    scrum_data = []
    for c in contributors:
        login = c['login']
        avatar_url = c['avatar_url']
        # Get recent PRs/commits
        commits_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits?author={login}&per_page=3"
        commit_resp = requests.get(commits_url, headers=headers)
        recent_commits = []
        if commit_resp.status_code == 200 and commit_resp.json():
            for commit in commit_resp.json():
                recent_commits.append({
                    'message': commit['commit']['message'],
                    'url': commit['html_url'],
                    'date': commit['commit']['author']['date']
                })
        scrum_data.append({
            'login': login,
            'avatar_url': avatar_url,
            'recent_commits': recent_commits
        })
    # Prepare prompt for OpenRouter
    prompt = """
You are an expert scrum master and GitHub project manager. Given the following contributors and their recent contributions (commits), generate:
- At most 2 new issue suggestions for each contributor, tailored to their expertise and recent work.
- For each contributor, list their old issues done (based on their recent commits), and assign the new issues.
- For each new issue, provide a short title, description, and a realistic timeline (in days) for completion.
- Only return at most 5 contributors. If you run out of space, do not include incomplete objects.
- Return the result as a valid JSON array of objects with: contributor, new_issues (list of {title, description, timeline_days}), old_issues_done (list of strings), and avatar_url.
"""
    for c in scrum_data[:5]:
        prompt += f"\nContributor: {c['login']}\nAvatar: {c['avatar_url']}\nRecent Commits:\n"
        for rc in c['recent_commits']:
            prompt += f"- {rc['message']} ({rc['date']})\n"
    prompt += "\nGenerate the scrum table as described."
    # Call OpenRouter
    openrouter_headers = {
        "Authorization": f"Bearer {get_openrouter_api_key()}",
        "Content-Type": "application/json"
    }
    print('DEBUG OpenRouter Authorization header:', openrouter_headers["Authorization"])
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful AI scrum master and GitHub project manager."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1200,
        "temperature": 0.7
    }
    resp = requests.post(OPENROUTER_API_URL, headers=openrouter_headers, json=payload)
    print('DEBUG OpenRouter response status:', resp.status_code)
    if resp.status_code != 200:
        return jsonify({'error': 'OpenRouter API error', 'details': resp.text}), 500
    # Try to extract JSON from the response
    try:
        content = resp.json()['choices'][0]['message']['content']
        import json as pyjson, re as pyre
        # Remove markdown code block if present
        content = content.strip()
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        scrum_table = pyjson.loads(content)
    except Exception as e:
        return jsonify({'error': 'Failed to parse OpenRouter response', 'details': str(e), 'raw': resp.text}), 500
    return jsonify({'scrum_table': scrum_table})

@analyzer_bp.route('/chat-with-repo', methods=['POST'])
def chat_with_repo():
    data = request.get_json()
    repo_url = data.get('repo_url')
    user_message = data.get('message')
    chat_history = data.get('history', [])

    if not repo_url or not user_message:
        return jsonify({'error': 'Missing repo_url or message'}), 400

    owner, repo = extract_owner_repo(repo_url)
    if not owner or not repo:
        return jsonify({'error': 'Invalid GitHub repo URL'}), 400

    try:
        # 1. Fetch context from the repository
        headers = {'Authorization': f'token {get_github_api_key()}'}
        contrib_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contributors"
        contrib_resp = requests.get(contrib_url, headers=headers)
        contrib_resp.raise_for_status()
        contributors = contrib_resp.json()[:5]

        context_summary = "Repository Context:\\n"
        for c in contributors:
            login = c['login']
            commits_url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits?author={login}&per_page=3"
            commit_resp = requests.get(commits_url, headers=headers)
            commit_resp.raise_for_status()
            recent_commits = commit_resp.json()
            context_summary += f"- Contributor: {login}\\n  Recent work:\\n"
            for commit in recent_commits:
                context_summary += f"  - {commit['commit']['message'].splitlines()[0]}\\n"

        # 2. Configure and call Gemini API
        genai.configure(api_key=get_gemini_api_key())
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Reformat history for Gemini
        gemini_history = []
        for item in chat_history:
            gemini_history.append({'role': 'user', 'parts': [item['user']]})
            if 'bot' in item and item['bot']:
                 gemini_history.append({'role': 'model', 'parts': [item['bot']]})

        chat = model.start_chat(history=gemini_history)
        
        prompt = f"""
        Based on the following repository context and our conversation history, please answer my question.
        
        {context_summary}
        
        Question: {user_message}
        """
        
        response = chat.send_message(prompt)
        
        return jsonify({'response': response.text})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch repository data: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred with the Gemini API: {str(e)}'}), 500 
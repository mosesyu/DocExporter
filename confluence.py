import requests
import os
from markdownify import markdownify as md
from config_utils import load_config

# Load configuration from JSON file
config = load_config()
confluence_config = config['confluence']

# Get personal access token from config
PERSONAL_ACCESS_TOKEN = confluence_config.get('personal_access_token')

if not PERSONAL_ACCESS_TOKEN or PERSONAL_ACCESS_TOKEN == "YOUR_TOKEN_HERE":
    raise ValueError("Please set your personal_access_token in the config.json file. Use https://confluence.sage.com/plugins/personalaccesstokens/usertokens.action to create a personal access token")

BASE_URL = confluence_config['base_url']
SPACE_KEY = confluence_config['space_key']
PAGE_TITLE = confluence_config['page_title']
EXPORT_DIR = confluence_config['export_dir']
MAX_NESTING_DEPTH = confluence_config['max_depth']

# Set up headers for authentication
headers = {
    "Authorization": f"Bearer {PERSONAL_ACCESS_TOKEN}",
    "Accept": "application/json"
}

# Step 1: Get the page ID
def get_page_id():
    url = f"{BASE_URL}/rest/api/content"
    params = {
        "title": PAGE_TITLE,
        "spaceKey": SPACE_KEY,
        "expand": "version"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    results = response.json().get("results", [])
    if not results:
        raise Exception("Page not found.")
    return results[0]["id"]

# Step 2: Get child pages (recursive)
def get_child_pages(parent_id):
    url = f"{BASE_URL}/rest/api/content/{parent_id}/child/page"
    params = {
        "expand": "body.storage"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("results", [])

# Step 2b: Get all nested child pages recursively with depth limit
def get_all_nested_pages(parent_id, all_pages=None, max_depth=MAX_NESTING_DEPTH, current_depth=0):
    if all_pages is None:
        all_pages = []
    
    # Safety check: stop if we've reached the maximum depth
    if current_depth >= max_depth:
        print(f"Warning: Reached maximum depth limit of {max_depth} levels. Stopping recursion.")
        return all_pages
    
    # Get direct children
    children = get_child_pages(parent_id)
    
    for child in children:
        print(f"Found page: {child['title']}")
        all_pages.append(child)
        # Recursively get children of this child with incremented depth
        get_all_nested_pages(child["id"], all_pages, max_depth, current_depth + 1)
    
    return all_pages

# Export each page to a file
def export_pages(pages):
    # Create export directory with space key subdirectory
    space_export_dir = os.path.join(EXPORT_DIR, SPACE_KEY)
    os.makedirs(space_export_dir, exist_ok=True)
    for page in pages:
        # Sanitize filename by replacing invalid characters
        title = page["title"]
        # Replace invalid Windows filename characters with underscores
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '/', '\\']
        for char in invalid_chars:
            title = title.replace(char, '_')
        # Remove multiple consecutive underscores and trim
        title = '_'.join(filter(None, title.split('_')))
        
        html_content = page["body"]["storage"]["value"]

        # Convert HTML to Markdown using markdownify
        markdown_content = md(html_content)

        filename = os.path.join(space_export_dir, f"{title}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Exported: {title}")

# Run the script
try:
    page_id = get_page_id()
    all_nested_pages = get_all_nested_pages(page_id)
    print(f"All nested pages under '{PAGE_TITLE}':")
    for page in all_nested_pages:
        print(f"- {page['title']} (ID: {page['id']})")
    export_pages(all_nested_pages)
except Exception as e:
    print("Error:", e)

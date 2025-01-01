import os
import requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from notion_client import Client

# Setup Notion Client
notion = Client(auth="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")  # Replace with your Notion API key

# Google Docs and Drive API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
]


def authenticate_google():
    """Authenticate and return Google services."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    
    # Build and return the services
    docs_service = build('docs', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    return docs_service, drive_service


# Authenticate Google services
docs_service, drive_service = authenticate_google()


def fetch_notion_content(page_id):
    """Fetch content from a Notion page."""
    response = notion.blocks.children.list(block_id=page_id)
    blocks = response.get("results", [])
    content = []

    def process_block(block):
        block_type = block.get("type")
        block_data = block.get(block_type, {})
        text_data = block_data.get("rich_text", [])

        if block_type == "paragraph":
            content.append("".join([text.get("plain_text", "") for text in text_data]))
        elif block_type == "heading_1":
            content.append({"type": "heading", "text": "".join([text.get("plain_text", "") for text in text_data]), "level": 1})
        elif block_type == "heading_2":
            content.append({"type": "heading", "text": "".join([text.get("plain_text", "") for text in text_data]), "level": 2})
        elif block_type == "heading_3":
            content.append({"type": "heading", "text": "".join([text.get("plain_text", "") for text in text_data]), "level": 3})
        elif block_type == "bulleted_list_item":
            content.append({"type": "list", "text": "".join([text.get("plain_text", "") for text in text_data]), "style": "bullet"})
        elif block_type == "numbered_list_item":
            content.append({"type": "list", "text": "".join([text.get("plain_text", "") for text in text_data]), "style": "number"})
        elif block_type == "quote":
            content.append({"type": "quote", "text": "".join([text.get("plain_text", "") for text in text_data])})
        elif block_type == "image":
            image_url = block_data.get("file", {}).get("url", "")
            if image_url:
                content.append({"type": "image", "url": image_url})
        else:
            content.append(f"[Unsupported block type: {block_type}]")

    for block in blocks:
        process_block(block)
    return content


def upload_image_to_drive(image_path):
    """Upload an image to Google Drive and return its ID."""
    file_metadata = {'name': os.path.basename(image_path)}
    media = MediaFileUpload(image_path, mimetype='image/png')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    # Make the file public by creating a permission for "anyone"
    try:
        drive_service.permissions().create(
            fileId=file['id'], 
            body={'role': 'reader', 'type': 'anyone'}
        ).execute()
    except HttpError as e:
        print(f"Error setting permissions: {e}")

    return file.get('id')


def download_image(image_url):
    """Download an image from a URL and save it locally."""
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        filename = "temp_image.png"
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    return None


def create_google_doc(title, content):
    """Create a Google Doc and update it with content and images."""
    doc = docs_service.documents().create(body={"title": title}).execute()
    doc_id = doc['documentId']
    requests = []

    for item in content:
        if isinstance(item, str):
            # Add plain text
            requests.append({"insertText": {"location": {"index": 1}, "text": item + "\n"}})
        elif isinstance(item, dict):
            if item.get("type") == "heading":
                # Add heading
                requests.append({
                    "insertText": {"location": {"index": 1}, "text": item["text"] + "\n"}
                })
                requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": 1, "endIndex": len(item["text"]) + 1},
                        "paragraphStyle": {"namedStyleType": f"HEADING_{item['level']}"},
                        "fields": "namedStyleType"
                    }
                })
            elif item.get("type") == "list":
                # Add list item
                requests.append({"insertText": {"location": {"index": 1}, "text": item["text"] + "\n"}})
            elif item.get("type") == "quote":
                # Add quote
                requests.append({
                    "insertText": {"location": {"index": 1}, "text": item["text"] + "\n"}
                })
            elif item.get("type") == "image":
                # Add image
                image_path = download_image(item["url"])
                if image_path:
                    drive_file_id = upload_image_to_drive(image_path)
                    os.remove(image_path)
                    image_uri = f"https://drive.google.com/uc?id={drive_file_id}"
                    requests.append({
                        "insertInlineImage": {
                            "location": {"index": 1},
                            "uri": image_uri
                        }
                    })

    docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()
    print(f"Google Doc created: https://docs.google.com/document/d/{doc_id}/edit")


# Replace with your Notion page ID and desired Google Doc title
NOTION_PAGE_ID = "15034f6b27ca80b98e42f21a5b801daf"  # Replace with your Notion page ID
GOOGLE_DOC_TITLE = "My Notion Notes"

notion_content = fetch_notion_content(NOTION_PAGE_ID)
create_google_doc(GOOGLE_DOC_TITLE, notion_content)

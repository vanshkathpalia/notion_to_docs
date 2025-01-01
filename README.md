# Notion to Google Docs Copier

## **Overview**

I created this project to solve the issue of downloading Notion pages, especially those containing images, as PDFs. The solution involves using the Notion API, Google Docs API, and Google Drive API to:

1. Copy data from a Notion page to a Google Docs document.
2. Download the Google Docs document as a PDF.

This project ensures seamless handling of text, images, and other supported content types from Notion to Google Docs.

---

## **Features**

- Fetch content from Notion pages, including text, images, and basic formatting.
- Transfer the content to Google Docs with proper formatting.
- Support for image uploads to Google Drive and embedding them in Google Docs.
- Download the Google Docs file as a PDF.

---

## **Setup Instructions**

### **1. Prerequisites**

- Python 3.7+
- A Notion API integration token
- Google Cloud Platform (GCP) project with Google Docs and Drive APIs enabled
- Credentials for Google APIs (`credentials.json` file)

### **2. Clone the Repository**

```bash
git clone https://github.com/<your-username>/notion-to-google-docs.git
cd notion-to-google-docs
```

### **3. Create a Notion Integration**

1. Go to [Notion Developers](https://www.notion.so/my-integrations).
2. Create a new integration and note the API key.
3. Share your Notion page with the integration.

### **4. Enable Google APIs**

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or use an existing one).
3. Enable the following APIs:
   - Google Docs API
   - Google Drive API
4. Create OAuth 2.0 credentials:
   - Download the `credentials.json` file.
   - Save it in the project directory.

### **5. Install Dependencies**

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### **6. Set Up Environment Variables**

1. Create a `.env` file in the project directory.
2. Add the following:

```env
NOTION_API_KEY=your_notion_api_key
GOOGLE_CREDENTIALS_PATH=credentials.json
```

### **7. Authenticate Google APIs**

Run the script to authenticate with Google APIs. This will generate a `token.json` file for future use.

```bash
python main.py
```

---

## **Usage**

1. Replace the `NOTION_PAGE_ID` in the script with your Notion page ID.
2. Run the script:

```bash
python main.py
```

3. The content from your Notion page will be copied to Google Docs, and you can download it as a PDF.

---

## **Supported Block Types**

Currently, the following Notion block types are supported:

- Paragraphs
- Headings (H1, H2, H3)
- Bulleted and numbered lists
- Quotes
- Images

Unsupported block types will be logged for further improvements.

---

## **Contributing**

Feel free to fork this repository and submit pull requests to enhance functionality or fix issues.

---

## **Security Notes**

- Never expose your `credentials.json`, `token.json`, or API keys in public repositories.
- Add sensitive files to `.gitignore` to prevent accidental commits.

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.

---

## **Contact**

For questions or feedback, please reach out at [your email/contact info].


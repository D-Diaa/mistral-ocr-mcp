# Mistral OCR MCP Server

A Model Context Protocol (MCP) server that provides Optical Character Recognition (OCR) capabilities using Mistral AI's document processing service. The primary use case is converting local PDF files to markdown format.

## Features

- **Local file processing**: Convert PDF/DOCX/PPTX files to markdown format
- Extract text from documents (PDF, PPTX, DOCX) and images (PNG, JPEG, AVIF)
- Process documents via URL or base64 encoding
- Preserve document structure in markdown format
- Support for image bounding boxes and base64 output
- Built on the MCP Python SDK for easy integration with LLMs

## Installation

### Option 1: Using uvx (Recommended)

The simplest way to use this MCP server is with `uvx`:

1. Clone this repository:
```bash
git clone https://github.com/D-Diaa/mistral-ocr-mcp.git
cd mistral-ocr-mcp
```

2. Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "Mistral OCR": {
      "command": "uvx",
      "args": [
        "--from", "/path/to/mistral-ocr-mcp",
        "mistral-ocr-mcp"
      ],
      "env": {
        "MISTRAL_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Option 2: Using MCP Install with uv

```bash
# Clone and install with editable package
git clone https://github.com/D-Diaa/mistral-ocr-mcp.git
cd mistral-ocr-mcp
mcp install server.py --name "Mistral OCR" --with-editable . -v MISTRAL_API_KEY=your_api_key_here
```

### Option 3: Traditional pip installation

1. Clone this repository:
```bash
git clone https://github.com/D-Diaa/mistral-ocr-mcp.git
cd mistral-ocr-mcp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file with your Mistral API key
echo "MISTRAL_API_KEY=your_api_key_here" > .env
```

## Usage

### Claude Desktop Integration

The server will automatically configure in Claude Desktop using any of the installation methods above.

### Cursor Integration

For Cursor IDE, add this server configuration to your MCP settings:

```json
{
  "mcpServers": {
    "mistral-ocr": {
      "command": "python",
      "args": ["/path/to/mistral-ocr-mcp/server.py"],
      "env": {
        "MISTRAL_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Development Mode

Run the server in development mode for testing:

```bash
mcp dev server.py
```

### Direct Execution

Run the server directly:

```bash
python server.py
```

## Available Tools

### `ocr_local_file` ⭐ **Primary Tool**
Process a local file and save the output as markdown.

**Parameters:**
- `file_path` (str): Path to the local file to process
- `output_path` (str, optional): Output path for markdown file (defaults to same name with .md extension)
- `include_image_base64` (bool, optional): Include base64 encoded images

**Returns:**
- `success` (bool): Whether processing succeeded
- `text` (str): Extracted markdown content
- `output_file` (str): Path to the generated markdown file
- `metadata` (dict): Processing details including pages processed

**Example:**
```python
result = ocr_local_file("paper.pdf")
# Creates paper.md in the same directory
# result["output_file"] contains the full path to paper.md
```

### `ocr_document_url`
Extract text from a document using a URL.

**Parameters:**
- `document_url` (str): URL to the document
- `include_image_base64` (bool, optional): Include base64 encoded images

### `ocr_document_base64`
Extract text from a base64 encoded document.

**Parameters:**
- `document_base64` (str): Base64 encoded document content
- `media_type` (str): MIME type of the document
- `include_image_base64` (bool, optional): Include base64 encoded images

### `ocr_image_url`
Extract text from an image using a URL.

**Parameters:**
- `image_url` (str): URL to the image
- `include_image_base64` (bool, optional): Include base64 encoded images

### `download_and_ocr`
Download and process a document/image from URL.

**Parameters:**
- `url` (str): URL to download and process
- `include_image_base64` (bool, optional): Include base64 encoded images

## Available Resources

### `mistral-ocr://supported-formats`
Information about supported document and image formats.

### `mistral-ocr://usage-examples`
Usage examples for the OCR tools.

## Supported Formats

**Documents:**
- PDF (.pdf)
- PowerPoint (.pptx)
- Word Documents (.docx)

**Images:**
- PNG (.png)
- JPEG (.jpg, .jpeg)
- AVIF (.avif)

## Example Response

```json
{
  "success": true,
  "text": "# Document Title\n\nExtracted text content in markdown format...",
  "output_file": "/path/to/output.md",
  "metadata": {
    "input_file": "/path/to/input.pdf",
    "output_file": "/path/to/output.md",
    "media_type": "application/pdf",
    "file_size_bytes": 1875210,
    "pages_processed": 22,
    "include_image_base64": false
  }
}
```

## Error Handling

All tools return a standardized response format with `success` boolean and error information when processing fails.

## Requirements

- Python 3.8+
- Mistral API key
- Internet connection for document/image URL processing
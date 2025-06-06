# Mistral OCR MCP Server

A Model Context Protocol (MCP) server that provides Optical Character Recognition (OCR) capabilities using Mistral AI's document processing service.

## Features

- Extract text from documents (PDF, PPTX, DOCX) and images (PNG, JPEG, AVIF)
- Process documents via URL or base64 encoding
- Preserve document structure in markdown format
- Support for image bounding boxes and base64 output
- Built on the MCP Python SDK for easy integration with LLMs

## Installation

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
cp .env.example .env
# Edit .env and add your Mistral API key
```


## Usage

### Development Mode

Run the server in development mode:

```bash
mcp dev mistral_ocr_mcp/server.py
```

### Claude Desktop Integration

Install the server for use with Claude Desktop:

```bash
mcp install mistral_ocr_mcp/server.py
```

### Direct Execution

Run the server directly:

```bash
python mistral_ocr_mcp/server.py
```

## Available Tools

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
  "metadata": {
    "document_url": "https://example.com/document.pdf",
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
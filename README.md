# Mistral OCR MCP Server

A Model Context Protocol (MCP) server that provides Optical Character Recognition (OCR) capabilities using Mistral AI's document processing service. This server focuses exclusively on processing local files and converting them to markdown format.

## Features

- **Local file processing only**: Convert PDF/DOCX/PPTX/PNG/JPEG/AVIF files to markdown format
- Extract text from local documents and images
- Preserve document structure in markdown format
- Support for image bounding boxes and base64 output
- Built on the MCP Python SDK for easy integration with LLMs
- Simple, focused tool for local OCR processing

## Installation

### Option 1: Using uvx (Recommended)

The simplest way to use this MCP server is with `uvx`:

1. Clone this repository:
```bash
git clone https://github.com/D-Diaa/mistral-ocr-mcp.git
cd mistral-ocr-mcp
```

```json
{
  "mcpServers": {
    "mistral-ocr": {
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
mcp install server.py --name "mistral-ocr" --with-editable . -v MISTRAL_API_KEY=your_api_key_here
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

## Available Tools

### `ocr_local_file` ⭐ **Only Tool**
Process a local file and save the output as markdown.

**Parameters:**

- `file_path` (str): Path to the local file to process
- `output_path` (str, optional): Output path for markdown file (defaults to same name with .md extension)
- `include_image_base64` (bool, optional): Include base64 encoded images

**Returns:**

- `success` (bool): Whether processing succeeded
- `output_file` (str): Path to the generated markdown file
- `metadata` (dict): Processing details including pages processed

**Example:**

```python
result = ocr_local_file("paper.pdf")
# Creates paper.md in the same directory
# result["output_file"] contains the full path to paper.md
```

## Available Resources

### `mistral-ocr://supported-formats`

Information about supported document and image formats.

### `mistral-ocr://usage-examples`

Usage examples for the OCR tool.

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
- Internet connection for Mistral API access

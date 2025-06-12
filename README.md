# Mistral OCR MCP Server

A Model Context Protocol (MCP) server that enables Claude to perform OCR (Optical Character Recognition) on local files using Mistral AI's document processing capabilities.

## Setup

1. **Get a Mistral API key** from [Mistral AI Console](https://console.mistral.ai/)

2. **Add to Claude Desktop config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mistral-ocr": {
      "command": "uvx",
      "args": ["--from", "/path/to/mistral-ocr-mcp", "mistral-ocr-mcp"],
      "env": {
        "MISTRAL_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Replace `/path/to/mistral-ocr-mcp` with the actual path to this directory.

## Usage

### `ocr_local_file`
Process local files with OCR and convert to markdown format.

- `file_path`: Path to the local file to process
- `output_path`: Optional output path for markdown file (defaults to same name with .md extension)  
- `include_image_base64`: Whether to include base64 encoded images in response

## Examples

```
Process this document with OCR: /path/to/document.pdf

Extract text from this image: /path/to/image.jpg

OCR this file and save to custom location: /path/to/input.png with output /path/to/output.md
```

## Troubleshooting

- **API key error**: Set `MISTRAL_API_KEY` in your environment
- **File not found**: Check that the file path exists and is accessible
- **Unsupported format**: Ensure the file is a supported image or document format
- **Rate limit**: Wait and try again
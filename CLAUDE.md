# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Installation Options

**Option 1: uvx (Recommended)**
- Install for Claude Desktop using uvx: Add to `claude_desktop_config.json`:
  ```json
  "Mistral OCR": {
    "command": "uvx",
    "args": ["--from", "/path/to/mistral-ocr-mcp", "mistral-ocr-mcp"],
    "env": {"MISTRAL_API_KEY": "your_api_key"}
  }
  ```

**Option 2: MCP Install with uv**
- Install with editable package: `mcp install server.py --name "Mistral OCR" --with-editable . -v MISTRAL_API_KEY=your_key`

**Option 3: Traditional**
- Install for Claude Desktop: `mcp install server.py`
- Install dependencies: `pip install -r requirements.txt`

### Development
- Run server in development mode: `mcp dev server.py`
- Direct execution: `python server.py`
- Run tests: `python test_server.py`
- Build package: `uv build`

### Testing
- Test setup and environment: `python test_server.py`
- Run pytest (if using): `pytest`

## Architecture

This is a Model Context Protocol (MCP) server that provides OCR capabilities using Mistral AI's document processing service. The architecture is built around the FastMCP framework.

### Core Components

**Server (`server.py`)**:
- Uses FastMCP to create an MCP server named "Mistral OCR"
- Initializes Mistral client with API key from environment
- Provides 1 main tool and 2 resources

**Tools Architecture**:
- `ocr_local_file`: Process local files and save markdown output locally

**Resources**:
- `mistral-ocr://supported-formats`: Static format information
- `mistral-ocr://usage-examples`: Usage examples

### Key Patterns

**Error Handling**: The tool returns standardized `{"success": bool, "error": str, "metadata": dict}` format

**Response Format**: Successful responses include `output_file` (path to generated markdown) and `metadata` with processing details

## Environment Setup

Required environment variable:
- `MISTRAL_API_KEY`: Mistral AI API key

Create `.env` file or set environment variable before running.

## Supported Formats

**Documents**: PDF, PPTX, DOCX
**Images**: PNG, JPEG, AVIF

The tool supports optional `include_image_base64` parameter for image extraction with bounding boxes.

## Local File Processing

The `ocr_local_file` tool is the only tool for processing local files:
- Takes a local file path and converts it to markdown
- Automatically determines output path (changes extension from original to .md)
- Supports custom output path via `output_path` parameter
- Returns both the extracted text and the local path to the generated markdown file

Example usage:
```python
result = ocr_local_file("paper.pdf")
# Creates paper.md in the same directory
# result["output_file"] contains the full path to paper.md
```
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development
- Run server in development mode: `mcp dev server.py`
- Install for Claude Desktop: `mcp install server.py`
- Direct execution: `python server.py`
- Run tests: `python test_server.py`

### Dependencies
- Install dependencies: `pip install -r requirements.txt`
- Install with dev dependencies: `pip install -e .[dev]`

### Testing
- Test setup and environment: `python test_server.py`
- Run pytest (if using): `pytest`

## Architecture

This is a Model Context Protocol (MCP) server that provides OCR capabilities using Mistral AI's document processing service. The architecture is built around the FastMCP framework.

### Core Components

**Server (`server.py`)**:
- Uses FastMCP to create an MCP server named "Mistral OCR"
- Initializes Mistral client with API key from environment
- Provides 4 main tools and 2 resources

**Tools Architecture**:
- `ocr_document_url`: Process documents via URL
- `ocr_document_base64`: Process base64-encoded documents  
- `ocr_image_url`: Process images via URL (async)
- `download_and_ocr`: Download and process from URL (async)

**Resources**:
- `mistral-ocr://supported-formats`: Static format information
- `mistral-ocr://usage-examples`: Usage examples

### Key Patterns

**Error Handling**: All tools return standardized `{"success": bool, "error": str, "metadata": dict}` format

**Async vs Sync**: Image processing and download tools are async; document URL/base64 tools are sync

**Response Format**: All successful responses include `text` (extracted content in markdown) and `metadata` with processing details

## Environment Setup

Required environment variable:
- `MISTRAL_API_KEY`: Mistral AI API key

Create `.env` file or set environment variable before running.

## Supported Formats

**Documents**: PDF, PPTX, DOCX
**Images**: PNG, JPEG, AVIF

All tools support optional `include_image_base64` parameter for image extraction with bounding boxes.
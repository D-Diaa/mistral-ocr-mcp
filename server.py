"""Mistral OCR MCP Server

Provides OCR capabilities using Mistral AI's document processing.
"""

import os
import base64
from typing import Dict, Any
from pathlib import Path

from mcp.server import FastMCP
from mistralai import Mistral
from dotenv import load_dotenv
import httpx

load_dotenv()

mcp = FastMCP("Mistral OCR")

# Initialize Mistral client
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY environment variable is required")

mistral_client = Mistral(api_key=api_key)


@mcp.tool()
def ocr_document_url(
    document_url: str,
    include_image_base64: bool = False
) -> Dict[str, Any]:
    """
    Extract text from a document using Mistral OCR via URL.
    
    Args:
        document_url: URL to the document (supports pdf, pptx, docx, png, jpeg, jpg, avif)
        include_image_base64: Whether to include base64 encoded images in response
    
    Returns:
        Dictionary containing extracted text and metadata
    """
    try:
        ocr_response = mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": document_url
            },
            include_image_base64=include_image_base64
        )
        
        return {
            "success": True,
            "text": ocr_response.text,
            "metadata": {
                "document_url": document_url,
                "include_image_base64": include_image_base64
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "metadata": {
                "document_url": document_url
            }
        }


@mcp.tool()
def ocr_document_base64(
    document_base64: str,
    media_type: str,
    include_image_base64: bool = False
) -> Dict[str, Any]:
    """
    Extract text from a base64 encoded document using Mistral OCR.
    
    Args:
        document_base64: Base64 encoded document content
        media_type: MIME type of the document (e.g., 'application/pdf', 'image/png')
        include_image_base64: Whether to include base64 encoded images in response
    
    Returns:
        Dictionary containing extracted text and metadata
    """
    try:
        # Use data URI format for base64 content
        data_uri = f"data:{media_type};base64,{document_base64}"
        
        ocr_response = mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": data_uri
            },
            include_image_base64=include_image_base64
        )
        
        # Extract markdown from all pages
        markdown_content = ""
        for page in ocr_response.pages:
            if page.markdown:
                markdown_content += page.markdown + "\n\n"
        
        return {
            "success": True,
            "text": markdown_content,
            "metadata": {
                "media_type": media_type,
                "include_image_base64": include_image_base64,
                "document_size_bytes": len(base64.b64decode(document_base64)),
                "pages_processed": len(ocr_response.pages)
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "metadata": {
                "media_type": media_type
            }
        }


@mcp.tool()
async def ocr_image_url(
    image_url: str,
    include_image_base64: bool = False
) -> Dict[str, Any]:
    """
    Extract text from an image using Mistral OCR via URL.
    
    Args:
        image_url: URL to the image (supports png, jpeg, jpg, avif)
        include_image_base64: Whether to include base64 encoded images in response
    
    Returns:
        Dictionary containing extracted text and metadata
    """
    try:
        ocr_response = mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": image_url
            },
            include_image_base64=include_image_base64
        )
        
        return {
            "success": True,
            "text": ocr_response.text,
            "metadata": {
                "image_url": image_url,
                "include_image_base64": include_image_base64
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "metadata": {
                "image_url": image_url
            }
        }


@mcp.tool()
async def download_and_ocr(
    url: str,
    include_image_base64: bool = False
) -> Dict[str, Any]:
    """
    Download a document/image from URL and process it with OCR.
    
    Args:
        url: URL to download and process
        include_image_base64: Whether to include base64 encoded images in response
    
    Returns:
        Dictionary containing extracted text and metadata
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            
            content_type = response.headers.get("content-type", "")
            content_base64 = base64.b64encode(response.content).decode()
            
            ocr_response = mistral_client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "document_base64",
                    "document_base64": content_base64,
                    "media_type": content_type
                },
                include_image_base64=include_image_base64
            )
            
            return {
                "success": True,
                "text": ocr_response.text,
                "metadata": {
                    "url": url,
                    "content_type": content_type,
                    "content_size_bytes": len(response.content),
                    "include_image_base64": include_image_base64
                }
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "metadata": {
                "url": url
            }
        }


@mcp.tool()
def ocr_local_file(
    file_path: str,
    output_path: str = None,
    include_image_base64: bool = False
) -> Dict[str, Any]:
    """
    Process a local file with OCR and save the output as markdown.
    
    Args:
        file_path: Path to the local file to process
        output_path: Optional output path for markdown file (defaults to same name with .md extension)
        include_image_base64: Whether to include base64 encoded images in response
    
    Returns:
        Dictionary containing extracted text, output file path, and metadata
    """
    try:
        # Validate input file exists
        input_file = Path(file_path)
        if not input_file.exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}",
                "metadata": {"file_path": file_path}
            }
        
        # Determine output path
        if output_path is None:
            output_file = input_file.with_suffix('.md')
        else:
            output_file = Path(output_path)
        
        # Read file and encode as base64
        with open(input_file, 'rb') as f:
            file_content = f.read()
        
        document_base64 = base64.b64encode(file_content).decode()
        
        # Determine media type based on file extension
        suffix = input_file.suffix.lower()
        media_type_map = {
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.avif': 'image/avif'
        }
        
        media_type = media_type_map.get(suffix)
        if not media_type:
            return {
                "success": False,
                "error": f"Unsupported file type: {suffix}",
                "metadata": {"file_path": file_path, "file_extension": suffix}
            }
        
        # Process with Mistral OCR using data URI format
        data_uri = f"data:{media_type};base64,{document_base64}"
        
        ocr_response = mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": data_uri
            },
            include_image_base64=include_image_base64
        )
        
        # Extract markdown from all pages
        markdown_content = ""
        for page in ocr_response.pages:
            if page.markdown:
                markdown_content += page.markdown + "\n\n"
        
        # Write markdown output to file
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return {
            "success": True,
            "text": markdown_content,
            "output_file": str(output_file.absolute()),
            "metadata": {
                "input_file": str(input_file.absolute()),
                "output_file": str(output_file.absolute()),
                "media_type": media_type,
                "file_size_bytes": len(file_content),
                "pages_processed": len(ocr_response.pages),
                "include_image_base64": include_image_base64
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "metadata": {
                "file_path": file_path,
                "output_path": output_path
            }
        }


@mcp.resource("mistral-ocr://supported-formats")
def get_supported_formats() -> str:
    """Get information about supported document and image formats."""
    return """# Mistral OCR Supported Formats

## Document Formats
- PDF (.pdf)
- PowerPoint (.pptx)
- Word Documents (.docx)

## Image Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)
- AVIF (.avif)

## Input Methods
- Document URL (direct link to file)
- Base64 encoded content
- Download from URL and process

## Output
- Extracted text in markdown format
- Preserved document structure (headers, paragraphs, lists, tables)
- Optional base64 encoded images with bounding boxes
"""


@mcp.resource("mistral-ocr://usage-examples")
def get_usage_examples() -> str:
    """Get usage examples for the OCR tools."""
    return """# Mistral OCR Usage Examples

## Process Document by URL
```
ocr_document_url("https://example.com/document.pdf")
```

## Process Base64 Document
```
ocr_document_base64(base64_content, "application/pdf")
```

## Process Image by URL
```
ocr_image_url("https://example.com/image.png")
```

## Download and Process
```
download_and_ocr("https://example.com/file.pdf")
```

## With Image Base64 Output
```
ocr_document_url("https://example.com/doc.pdf", include_image_base64=True)
```
"""


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
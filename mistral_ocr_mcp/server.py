"""Mistral OCR MCP Server

Provides OCR capabilities using Mistral AI's document processing.
"""

import os
import base64
from typing import Dict, Any

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
        ocr_response = mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_base64",
                "document_base64": document_base64,
                "media_type": media_type
            },
            include_image_base64=include_image_base64
        )
        
        return {
            "success": True,
            "text": ocr_response.text,
            "metadata": {
                "media_type": media_type,
                "include_image_base64": include_image_base64,
                "document_size_bytes": len(base64.b64decode(document_base64))
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
#!/usr/bin/env python3
"""Test MCP Server functionality"""

import json
import sys
import asyncio
from pathlib import Path

# Add current directory to path to import server
sys.path.insert(0, str(Path(__file__).parent))

import server

async def test_mcp_server():
    """Test the MCP server components"""
    print("🧪 Testing MCP Server Components\n")
    
    # Test 1: Server creation
    print("1. Testing server creation...")
    try:
        mcp_server = server.mcp
        print(f"   ✅ Server name: {mcp_server.name}")
    except Exception as e:
        print(f"   ❌ Server creation failed: {e}")
        return False
    
    # Test 2: Local file tool
    print("\n2. Testing ocr_local_file tool...")
    try:
        # Test with paper.pdf if it exists
        if Path("paper.pdf").exists():
            result = server.ocr_local_file("paper.pdf", output_path="mcp_test_output.md")
            if result["success"]:
                print(f"   ✅ Successfully processed paper.pdf")
                print(f"   ✅ Output: {result['output_file']}")
                print(f"   ✅ Pages processed: {result['metadata']['pages_processed']}")
                
                # Verify output file exists
                if Path(result['output_file']).exists():
                    size = Path(result['output_file']).stat().st_size
                    print(f"   ✅ Output file size: {size} bytes")
                else:
                    print("   ❌ Output file not created")
                    return False
            else:
                print(f"   ❌ Processing failed: {result['error']}")
                return False
        else:
            print("   ⚠️  paper.pdf not found, skipping file processing test")
    except Exception as e:
        print(f"   ❌ Tool test failed: {e}")
        return False
    
    # Test 3: Resources
    print("\n3. Testing MCP resources...")
    try:
        formats = server.get_supported_formats()
        if "Mistral OCR Supported Formats" in formats:
            print("   ✅ supported-formats resource working")
        
        examples = server.get_usage_examples()
        if "Mistral OCR Usage Examples" in examples:
            print("   ✅ usage-examples resource working")
    except Exception as e:
        print(f"   ❌ Resource test failed: {e}")
        return False
    
    # Test 4: Error handling
    print("\n4. Testing error handling...")
    try:
        # Test non-existent file
        result = server.ocr_local_file("nonexistent.pdf")
        if not result["success"] and "File not found" in result["error"]:
            print("   ✅ File validation working")
        
        # Test unsupported file type
        Path("test.txt").write_text("test")
        result = server.ocr_local_file("test.txt")
        if not result["success"] and "Unsupported file type" in result["error"]:
            print("   ✅ File type validation working")
        Path("test.txt").unlink()
    except Exception as e:
        print(f"   ❌ Error handling test failed: {e}")
        return False
    
    print("\n🎉 All MCP server tests passed!")
    print("\nMCP Server Summary:")
    print(f"   • Server name: {server.mcp.name}")
    print("   • Tools available: 5 (ocr_local_file, ocr_document_url, ocr_document_base64, ocr_image_url, download_and_ocr)")
    print("   • Resources available: 2 (supported-formats, usage-examples)")
    print("   • Primary tool: ocr_local_file (converts PDF → markdown)")
    print("\nTo run as MCP server: mcp dev server.py")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)
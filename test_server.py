#!/usr/bin/env python3
"""Test script for Mistral OCR MCP Server"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_env_setup():
    """Test that environment is properly configured."""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        print("❌ MISTRAL_API_KEY not found in environment")
        print("Please create a .env file with your Mistral API key")
        return False
    
    print("✅ MISTRAL_API_KEY found")
    print(f"   Key starts with: {api_key[:8]}...")
    return True

def test_imports():
    """Test that all required packages can be imported."""
    try:
        from mcp.server import FastMCP
        print("✅ MCP SDK imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import MCP SDK: {e}")
        return False
    
    try:
        from mistralai import Mistral
        print("✅ Mistral AI client imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Mistral AI client: {e}")
        return False
    
    try:
        import httpx
        print("✅ HTTPX imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import HTTPX: {e}")
        return False
    
    return True

def test_server_creation():
    """Test that the server can be created."""
    try:
        from mistral_ocr_mcp.server import mcp
        print("✅ MCP server created successfully")
        print(f"   Server name: {mcp.name}")
        return True
    except Exception as e:
        print(f"❌ Failed to create MCP server: {e}")
        return False

async def main():
    """Run all tests."""
    print("🧪 Testing Mistral OCR MCP Server Setup\n")
    
    tests = [
        ("Environment Setup", test_env_setup),
        ("Package Imports", test_imports),
        ("Server Creation", test_server_creation),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The server is ready to use.")
        print("\nTo run the server:")
        print("  mcp dev mistral_ocr_mcp/server.py")
    else:
        print("❌ Some tests failed. Please check the setup.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Set up .env file with MISTRAL_API_KEY")

if __name__ == "__main__":
    asyncio.run(main())
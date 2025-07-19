#!/usr/bin/env python3
"""
Simple test script for the Items API
Run this after starting the API server to test all endpoints
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        print("✅ Root endpoint working")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False
    return True

def test_get_all_items():
    """Test getting all items"""
    print("\nTesting GET /items...")
    try:
        response = requests.get(f"{BASE_URL}/items")
        assert response.status_code == 200
        items = response.json()
        print(f"✅ GET /items working - Found {len(items)} items")
        if items:
            print(f"Sample item: {items[0]}")
    except Exception as e:
        print(f"❌ GET /items failed: {e}")
        return False
    return True

def test_create_item():
    """Test creating a new item"""
    print("\nTesting POST /items...")
    test_item = {
        "name": f"Test Item {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "description": "This is a test item created by the test script"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/items", json=test_item)
        assert response.status_code == 201
        created_item = response.json()
        print("✅ POST /items working")
        print(f"Created item: {created_item}")
        return created_item["id"]
    except Exception as e:
        print(f"❌ POST /items failed: {e}")
        return None

def test_get_specific_item(item_id):
    """Test getting a specific item by ID"""
    print(f"\nTesting GET /items/{item_id}...")
    try:
        response = requests.get(f"{BASE_URL}/items/{item_id}")
        assert response.status_code == 200
        item = response.json()
        print("✅ GET /items/{id} working")
        print(f"Retrieved item: {item}")
    except Exception as e:
        print(f"❌ GET /items/{item_id} failed: {e}")
        return False
    return True

def test_create_duplicate_item():
    """Test creating a duplicate item (should fail)"""
    print("\nTesting duplicate item creation...")
    duplicate_item = {
        "name": "Duplicate Test Item",
        "description": "This should create the first item"
    }
    
    try:
        # Create first item
        response = requests.post(f"{BASE_URL}/items", json=duplicate_item)
        assert response.status_code == 201
        print("✅ First item created successfully")
        
        # Try to create duplicate
        response = requests.post(f"{BASE_URL}/items", json=duplicate_item)
        assert response.status_code == 409
        print("✅ Duplicate detection working - got 409 Conflict")
        print(f"Error response: {response.json()}")
    except Exception as e:
        print(f"❌ Duplicate test failed: {e}")
        return False
    return True

def test_get_nonexistent_item():
    """Test getting a non-existent item (should return 404)"""
    print("\nTesting non-existent item retrieval...")
    try:
        response = requests.get(f"{BASE_URL}/items/99999")
        assert response.status_code == 404
        print("✅ 404 handling working")
        print(f"Error response: {response.json()}")
    except Exception as e:
        print(f"❌ 404 test failed: {e}")
        return False
    return True

def test_invalid_item_creation():
    """Test creating an item with invalid data"""
    print("\nTesting invalid item creation...")
    invalid_item = {
        "name": "",  # Empty name should fail
        "description": "This should fail due to empty name"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/items", json=invalid_item)
        assert response.status_code == 422
        print("✅ Input validation working - got 422 Unprocessable Entity")
        print(f"Validation error: {response.json()}")
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False
    return True

def main():
    """Run all tests"""
    print("🚀 Starting API tests...")
    print(f"Testing API at: {BASE_URL}")
    print("Make sure the API server is running before running this script!")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 7
    
    # Run all tests
    if test_root_endpoint():
        tests_passed += 1
    
    if test_get_all_items():
        tests_passed += 1
    
    created_item_id = test_create_item()
    if created_item_id:
        tests_passed += 1
        
        if test_get_specific_item(created_item_id):
            tests_passed += 1
    else:
        print("❌ Skipping GET specific item test due to creation failure")
    
    if test_create_duplicate_item():
        tests_passed += 1
    
    if test_get_nonexistent_item():
        tests_passed += 1
    
    if test_invalid_item_creation():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"🏁 Test Summary: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
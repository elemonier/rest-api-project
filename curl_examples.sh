#!/bin/bash

# Items API - curl Examples
# Make sure the API server is running on http://localhost:8000

echo "🚀 Items API - curl Examples"
echo "=============================="

BASE_URL="http://localhost:8000"

echo ""
echo "1. Test root endpoint"
echo "curl -X GET \"$BASE_URL/\""
curl -X GET "$BASE_URL/" | jq '.' 2>/dev/null || curl -X GET "$BASE_URL/"

echo ""
echo ""
echo "2. Get all items (initially empty)"
echo "curl -X GET \"$BASE_URL/items\""
curl -X GET "$BASE_URL/items" | jq '.' 2>/dev/null || curl -X GET "$BASE_URL/items"

echo ""
echo ""
echo "3. Create a new item"
echo "curl -X POST \"$BASE_URL/items\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"name\": \"Sample Item\", \"description\": \"This is a sample item\"}'"
curl -X POST "$BASE_URL/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Sample Item", "description": "This is a sample item"}' | jq '.' 2>/dev/null || \
curl -X POST "$BASE_URL/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Sample Item", "description": "This is a sample item"}'

echo ""
echo ""
echo "4. Create another item"
echo "curl -X POST \"$BASE_URL/items\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"name\": \"Another Item\", \"description\": \"Another test item\"}'"
curl -X POST "$BASE_URL/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Another Item", "description": "Another test item"}' | jq '.' 2>/dev/null || \
curl -X POST "$BASE_URL/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Another Item", "description": "Another test item"}'

echo ""
echo ""
echo "5. Get all items (should now show created items)"
echo "curl -X GET \"$BASE_URL/items\""
curl -X GET "$BASE_URL/items" | jq '.' 2>/dev/null || curl -X GET "$BASE_URL/items"

echo ""
echo ""
echo "6. Get specific item by ID (assuming ID 1 exists)"
echo "curl -X GET \"$BASE_URL/items/1\""
curl -X GET "$BASE_URL/items/1" | jq '.' 2>/dev/null || curl -X GET "$BASE_URL/items/1"

echo ""
echo ""
echo "7. Try to create duplicate item (should fail with 409)"
echo "curl -X POST \"$BASE_URL/items\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"name\": \"Sample Item\", \"description\": \"Duplicate item\"}'"
curl -X POST "$BASE_URL/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Sample Item", "description": "Duplicate item"}' | jq '.' 2>/dev/null || \
curl -X POST "$BASE_URL/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "Sample Item", "description": "Duplicate item"}'

echo ""
echo ""
echo "8. Try to get non-existent item (should fail with 404)"
echo "curl -X GET \"$BASE_URL/items/99999\""
curl -X GET "$BASE_URL/items/99999" | jq '.' 2>/dev/null || curl -X GET "$BASE_URL/items/99999"

echo ""
echo ""
echo "9. Try to create item with invalid data (should fail with 422)"
echo "curl -X POST \"$BASE_URL/items\" \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"name\": \"\", \"description\": \"Empty name should fail\"}'"
curl -X POST "$BASE_URL/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "", "description": "Empty name should fail"}' | jq '.' 2>/dev/null || \
curl -X POST "$BASE_URL/items" \
     -H "Content-Type: application/json" \
     -d '{"name": "", "description": "Empty name should fail"}'

echo ""
echo ""
echo "✅ curl examples completed!"
echo ""
echo "📖 Access interactive API documentation at:"
echo "   Swagger UI: $BASE_URL/docs"
echo "   ReDoc:      $BASE_URL/redoc"
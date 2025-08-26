#!/bin/bash

echo "🔥 Testing Flask Game Catalog API..."

# 1. POST - Add a new game
echo -e "\n📦 Adding a new game:"
curl -X POST http://localhost:5050/catalog \
-H "Content-Type: application/json" \
-d '{
  "name": "Celeste",
  "description": "A beautifully crafted platformer.",
  "price": 19.99,
  "rating": 9.5,
  "platform": "Multi",
  "release_date": "2018-01-25",
  "category": "Platformer",
  "quantity": 10
}'
echo -e "\n✅ Game added."

# 2. GET - Get all catalog items
echo -e "\n📚 Getting all catalog items:"
curl http://localhost:5050/catalog

# 3. PUT - Update quantity of a specific item (e.g., ID 21)
echo -e "\n✏️ Updating quantity for item ID 21:"
curl -X PUT http://localhost:5050/catalog/21 \
-H "Content-Type: application/json" \
-d '{"quantity": 100}'

# 4. GET - Retrieve the updated item
echo -e "\n🔍 Getting item with ID 21:"
curl http://localhost:5050/catalog/21

# 5. DELETE - Delete the item
echo -e "\n❌ Deleting item with ID 21:"
curl -X DELETE http://localhost:5050/catalog/21

# 6. GET - Confirm it's deleted
echo -e "\n🔁 Getting all items again to confirm deletion:"
curl http://localhost:5050/catalog

echo -e "\n✅ All tests completed.\n"

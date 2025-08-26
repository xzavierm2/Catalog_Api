# catalog_api.py

from flask import Flask, jsonify, request
from fetch_data import fetch_games
import catalog  # Import your core catalog.py module

app = Flask(__name__)

# Endpoint to get all items in the catalog, with optional filters
@app.route('/api/catalog', methods=['GET'])
def api_get_catalog():
    category = request.args.get('category')
    genre = request.args.get('genre')

    results = catalog.get_all_items()

    if category:
        results = [item for item in results if item.get("category") == category]
    if genre:
        results = [item for item in results if item.get("genre") == genre]

    return jsonify(results)

# Endpoint to fetch games from the external API and add them to the catalog
@app.route('/api/fetch_games', methods=['POST'])
def api_fetch_games():
    new_games = fetch_games()
    # Assuming fetch_games returns a list of games ready for catalog
    # Add each new game to catalog using catalog.add_item for ID and persistence
    added_items = []
    for game in new_games:
        added_item = catalog.add_item(game)
        added_items.append(added_item)
    return jsonify({"message": f"Fetched and added {len(added_items)} games"}), 200

# Endpoint to add a new item to the catalog
@app.route('/api/catalog', methods=['POST'])
def api_add_item():
    item = request.get_json()
    if not item or "name" not in item:
        return jsonify({"error": "Invalid input: 'name' is required"}), 400
    new_item = catalog.add_item(item)
    return jsonify(new_item), 201

# Endpoint to get an item by ID
@app.route('/api/catalog/<int:item_id>', methods=['GET'])
def api_get_item(item_id):
    item = catalog.get_item(item_id)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

# Endpoint to delete an item by ID
@app.route('/api/catalog/<int:item_id>', methods=['DELETE'])
def api_delete_item(item_id):
    item = catalog.get_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    catalog.delete_item(item_id)
    return jsonify({"message": "Item deleted"})

# Endpoint to get all unique categories
@app.route('/api/catalog/categories', methods=['GET'])
def api_get_categories():
    categories = sorted(set(item.get("category", "") for item in catalog.get_all_items() if item.get("category")))
    return jsonify(categories)

# Endpoint to get all unique genres
@app.route('/api/catalog/genres', methods=['GET'])
def api_get_genres():
    genres = sorted(set(item.get("genre", "") for item in catalog.get_all_items() if item.get("genre")))
    return jsonify(genres)

# Endpoint to update an item by ID
@app.route('/api/catalog/<int:item_id>', methods=['PUT'])
def api_update_item(item_id):
    item = catalog.get_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    updated_data = request.get_json()
    # Update item fields using catalog.update_item with unpacked dictionary
    updated_item = catalog.update_item(
        item_id,
        name=updated_data.get("name", item.get("name")),
        description=updated_data.get("description", item.get("description")),
        price=updated_data.get("price", item.get("price")),
        quantity=updated_data.get("quantity", item.get("quantity")),
        rating=updated_data.get("rating", item.get("rating")),
        platform=updated_data.get("platform", item.get("platform")),
        category=updated_data.get("category", item.get("category")),
        genre=updated_data.get("genre", item.get("genre")),
        release_date=updated_data.get("release_date", item.get("release_date"))
    )
    return jsonify(updated_item)

# Endpoint to search by name or description
@app.route('/api/catalog/search', methods=['GET'])
def api_search_items():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify([])  # Or return error

    results = [item for item in catalog.get_all_items()
               if query in item.get("name", "").lower() or query in item.get("description", "").lower()]
    return jsonify(results)

# Endpoint to filter by release year or minimum rating
@app.route('/api/catalog/filter', methods=['GET'])
def api_filter_items():
    release_year = request.args.get('release_year')
    min_rating = request.args.get('min_rating', type=float)

    results = catalog.get_all_items()

    if release_year:
        results = [item for item in results if item.get("release_date", "").startswith(release_year)]
    if min_rating is not None:
        results = [item for item in results if float(item.get("rating", 0)) >= min_rating]

    return jsonify(results)

if __name__ == '__main__':
    catalog.load_items_from_file()  # Load catalog on startup from catalog.py's loader
    app.run(debug=True)

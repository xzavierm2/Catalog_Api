
# app.py
from flask import Flask, request, jsonify, abort
from flasgger import Swagger
import catalog

app = Flask(__name__)

# Swagger configuration
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Game Catalog API",
        "description": "API for managing a video game catalog with search, CRUD, and rating features.",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"],
    "definitions": {
        "Game": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "name": {"type": "string", "example": "The Legend of Zelda: Breath of the Wild"},
                "platform": {"type": "string", "example": "Nintendo Switch"},
                "release_date": {"type": "string", "example": "2017-03-03"},
                "genre": {"type": "string", "example": "Action-adventure"},
                "category": {"type": "string", "example": "Adventure"},
                "description": {"type": "string", "example": "An open-world action-adventure game set in a vast world."},
                "price": {"type": "number", "example": 59.99},
                "quantity": {"type": "integer", "example": 100},
                "rating": {"type": "number", "example": 9.5}
            }
        }
    }
})

# ---- Example in-memory games list ---- #
games = [
    {
        "id": 1,
        "name": "The Legend of Zelda: Breath of the Wild",
        "platform": "Nintendo Switch",
        "release_date": "2017-03-03",
        "genre": "Action-adventure",
        "category": "Adventure",
        "description": "An open-world action-adventure game set in a vast world.",
        "price": 59.99,
        "quantity": 100,
        "rating": 9.5
    },
    {
        "id": 2,
        "name": "Super Mario Odyssey",
        "platform": "Nintendo Switch",
        "release_date": "2017-10-27",
        "genre": "Platformer",
        "category": "Adventure",
        "description": "A platform game featuring Mario on a globe-trotting adventure.",
        "price": 59.99,
        "quantity": 50,
        "rating": 9.0
    }
]

# ---- Games endpoints ---- #
@app.route('/games', methods=['POST'])
def add_game():
    """Add a new game to the catalog
    ---
    tags:
      - Games
    parameters:
      - name: game
        in: body
        required: true
        schema:
          $ref: '#/definitions/Game'
    responses:
      201:
        description: Game added successfully
        schema:
          $ref: '#/definitions/Game'
    """
    if not request.json or 'name' not in request.json:
        abort(400, description="Invalid input")
    
    new_game = {
        "id": len(games) + 1,
        "name": request.json['name'],
        "platform": request.json.get('platform', 'Multi'),
        "release_date": request.json.get('release_date', ''),
        "genre": request.json.get('genre', ''),
        "category": request.json.get('category', ''),
        "description": request.json.get('description', ''),
        "price": request.json.get('price', 0.0),
        "quantity": request.json.get('quantity', 0),
        "rating": request.json.get('rating', 0.0)
    }
    
    games.append(new_game)
    return jsonify(new_game), 201

@app.route('/games', methods=['GET'])
def get_games():
    """Get all games in memory
    ---
    tags:
      - Games
    responses:
      200:
        description: A list of games
        schema:
          type: array
          items:
            $ref: '#/definitions/Game'
    """
    return jsonify(games), 200

@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    """Delete a game by ID
    ---
    tags:
      - Games
    parameters:
      - name: game_id
        in: path
        type: integer
        required: true
        description: ID of the game to delete
    responses:
      200:
        description: Game deleted successfully
      404:
        description: Game not found
    """
    for game in games:
        if game["id"] == game_id:
            games.remove(game)
            return jsonify({"message": f"Game with ID {game_id} deleted"}), 200
    return jsonify({"error": "Game not found"}), 404

# ---- Catalog endpoints (CRUD + search) ---- #
@app.route("/catalog", methods=["GET"])
def get_catalog():
    """Get all catalog items"""
    return jsonify(catalog.get_all_items()), 200

@app.route("/catalog/<int:item_id>", methods=["GET"])
def get_catalog_item(item_id):
    """Get a catalog item by ID"""
    item = catalog.get_item(item_id)
    if item:
        return jsonify(item)
    abort(404, description="Item not found")

@app.route("/catalog", methods=["POST"])
def add_catalog_item():
    """Add a new catalog item"""
    if not request.json or 'name' not in request.json:
        abort(400, description="Invalid input")
    item_data = {k: request.json.get(k, "") for k in ['name','description','price','quantity','rating','platform','release_date','genre','category']}
    missing = [f for f in ['name','price','quantity'] if not item_data.get(f)]
    if missing:
        abort(400, description=f"Missing required fields: {', '.join(missing)}")
    new_item = catalog.add_item(item_data)
    return jsonify(new_item), 201

@app.route("/catalog/<int:item_id>", methods=["PUT"])
def update_catalog_item(item_id):
    """Update an existing catalog item"""
    item = catalog.get_item(item_id)
    if not item:
        abort(404, description="Item not found")
    updated_data = {k: request.json.get(k, item[k]) for k in item.keys()}
    updated_item = catalog.update_item(item_id, **updated_data)
    return jsonify(updated_item), 200

@app.route("/catalog/<int:item_id>", methods=["DELETE"])
def delete_catalog_item(item_id):
    """Delete a catalog item by ID"""
    item = catalog.get_item(item_id)
    if not item:
        abort(404, description="Item not found")
    catalog.delete_item(item_id)
    return jsonify({"message": "Item deleted successfully"}), 200

@app.route("/catalog/search", methods=["GET"])
def search_catalog_items():
    """Search catalog items by name query"""
    query = request.args.get("query", "")
    if not query:
        abort(400, description="Query parameter is required")
    results = catalog.search_items(query)
    return jsonify(results), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)


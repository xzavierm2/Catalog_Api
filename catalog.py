#Logic for storing and managing catalog items

# Catalog.py

import json
import os

catalog = []    # List to store catalog items
next_id = 1     # Variable to keep track of the next available ID

def add_item(item_data):
    global next_id
    item_data.setdefault("quantity", 1)  # Ensure quantity is set before assigning ID
    item_data["id"] = next_id
    next_id += 1
    catalog.append(item_data)
    save_items_to_file()  # Save the updated catalog to file
    return item_data

def search_by_rating_range(rating_input):
    global catalog
    print(f"[DEBUG] Items loaded: {len(catalog)}")

    MAX_RATING = 10.0
    MIN_RATING = 0.0

    try:
        if "-" in rating_input:
            min_rating, max_rating = map(float, rating_input.split("-"))
            if min_rating > max_rating:  # Swap if reversed
                min_rating, max_rating = max_rating, min_rating
            min_rating = max(MIN_RATING, min_rating)
            max_rating = min(MAX_RATING, max_rating)
        else:
            center = float(rating_input)
            if center < 0 or center > 10:
                print(f"[DEBUG] Rating {center} out of valid range 0-10")
                return []
            min_rating = max(center - 0.5, MIN_RATING)
            max_rating = min(center + 0.49, MAX_RATING)
    except ValueError:
        print("Invalid rating input. Please enter a valid float or range (e.g. 2.25 or 1-3).")
        return []

    results = []
    for item in catalog:
        try:
            rating = float(item.get("rating", 0))
            print(f"[DEBUG] Checking item {item['name']} with rating {rating}")
        except (ValueError, TypeError):
            continue

        if min_rating <= rating <= max_rating:
            results.append(item)

    print(f"[DEBUG] Found {len(results)} items with rating between {min_rating} and {max_rating}.")
    return results



def get_item(item_id):
    for item in catalog:
        if item["id"] == item_id:
            return item
    return None

def get_all_items():
    return sorted(catalog, key=lambda x: x["name"].lower())

def search_items(query, field="name"):
    results = []
    for item in get_all_items():
        if field == "rating":
            try:
                if float(item.get("rating", 0)) >= float(query):
                    results.append(item)
            except (ValueError, TypeError):
                continue
        else:
            value = str(item.get(field, "")).lower()
            if query.lower() in value:
                results.append(item)
    return results

def update_item(item_id, name=None, description=None, price=None, quantity=None, rating=None, platform="Multi", category=None, genre=None, release_date=None):
    item = get_item(item_id)
    if item:
        if name is not None:
            item["name"] = name
        if description is not None:
            item["description"] = description
        if price is not None:
            item["price"] = price
        if quantity is not None:
            item["quantity"] = quantity
        if rating is not None:
            item["rating"] = rating
        if platform is not None:
            item["platform"] = platform
        if release_date is not None:
            item["release_date"] = release_date
        if category is not None:
            item["category"] = category
        if genre is not None:
            item["genre"] = genre
        save_items_to_file()
        return item
    return None

def delete_item(item_id):
    global catalog
    catalog = [item for item in catalog if item["id"] != item_id]
    save_items_to_file()  # Save the updated catalog to file
    return catalog

def update_item_quantity(item_id, quantity):
    item = get_item(item_id)
    if item:
        item["quantity"] = quantity
        return item
    return None

def get_item_by_name(name):
    for item in catalog:
        if item["name"].lower() == name.lower():
            return item
    return None

def get_items_by_rating(ascending=False):
    return sorted(catalog, key=lambda x: x.get("rating", 0), reverse=not ascending)

def get_items_by_platform(platform):
    results = []
    for item in catalog:
        if item.get("platform") == platform:
            results.append(item)
    return results

def get_items_by_genre(genre):
    results = []
    for item in catalog:
        if item.get("genre") == genre:
            results.append(item)
    return results

def get_items_by_category(category):
    results = []
    for item in catalog:
        if item.get("category") == category:
            results.append(item)
    return results

def get_items_by_price_range(min_price, max_price):
    results = []
    for item in catalog:
        if min_price <= item["price"] <= max_price:
            results.append(item)
    return results

def get_items_by_criteria(name=None, category=None, min_price=None, max_price=None):
    results = []
    for item in catalog:
        if (name is None or name.lower() in item["name"].lower()) and \
           (category is None or item.get("category") == category) and \
           (min_price is None or item["price"] >= min_price) and \
           (max_price is None or item["price"] <= max_price):
            results.append(item)
    return results

def get_items_sorted_by_price(ascending=True):
    return sorted(catalog, key=lambda x: x["price"], reverse=not ascending)

def load_items_from_file(filename="catalog_data.json"):
    global catalog, next_id
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            catalog = data.get("catalog", [])
            next_id = max(item["id"] for item in catalog) + 1 if catalog else 1
            for item_data in catalog:
                item_data.setdefault("quantity", 1)
    else:
        catalog = []
        next_id = 1

# Load items from the JSON file at startup
load_items_from_file()

def save_items_to_file(filename="catalog_data.json"):
    with open(filename, 'w') as file:
        json.dump({"catalog": catalog}, file, indent=4)

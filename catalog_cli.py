# catalog-cli.py


import catalog


# Simple CLI for interacting with the catalog module
def print_item(item):
    print(f"ID: {item['id']}")
    print(f"Name: {item['name']}")
    print(f"Description: {item.get('description', '')}")
    print(f"Price: ${item.get('price', 0):.2f}")
    print(f"Quantity: {item.get('quantity', 0)}")
    print(f"Rating: {item.get('rating', 0)}")
    print(f"Platform: {item.get('platform', 'Multi')}")
    print(f"Release Date: {item.get('release_date', '')}")
    print(f"Category: {item.get('category', '')}")
    print(f"Genre: {item.get('genre', '')}")
    print("-" * 30)

# List all items
def list_items():
    items = catalog.get_all_items()
    if not items:
        print("Catalog is empty.")
    else:
        for item in items:
            print_item(item)
# Add a new item
def add_item():
    try:
        name = input("Name: ").strip()
        description = input("Description: ").strip()
        price = float(input("Price: "))
        quantity = int(input("Quantity: "))
        rating = float(input("Rating: "))
        platform = input("Platform: ").strip()
        release_date = input("Release Date (YYYY-MM-DD): ").strip()
        category = input("Category: ").strip()
        genre = input("Genre: ").strip()
    except ValueError:
        print("Invalid input for numeric fields. Please try again.")
        return

    item_data = {
        "name": name,
        "description": description,
        "price": price,
        "quantity": quantity,
        "rating": rating,
        "platform": platform,
        "release_date": release_date,
        "category": category,
        "genre": genre
    }
    new_item = catalog.add_item(item_data)
    print("Added new item:")
    print_item(new_item)

# Update an existing item
def update_item():
    try:
        item_id = int(input("Enter the ID of the item to update: "))
    except ValueError:
        print("Invalid ID. Please enter a numeric value.")
        return

    item = catalog.get_item(item_id)
    if not item:
        print("Item not found.")
        return

    print("Leave blank to keep current value.")
    name = input(f"Name [{item['name']}]: ").strip() or item['name']
    description = input(f"Description [{item.get('description', '')}]: ").strip() or item.get('description', '')
    
    price_input = input(f"Price [{item.get('price', 0)}]: ").strip()
    price = float(price_input) if price_input else item.get('price', 0)

    quantity_input = input(f"Quantity [{item.get('quantity', 0)}]: ").strip()
    quantity = int(quantity_input) if quantity_input else item.get('quantity', 0)

    rating_input = input(f"Rating [{item.get('rating', 0)}]: ").strip()
    rating = int(rating_input) if rating_input else item.get('rating', 0)

    platform = input(f"Platform [{item.get('platform', 'Multi')}]: ").strip() or item.get('platform', 'Multi')
    release_date = input(f"Release Date [{item.get('release_date', '')}]: ").strip() or item.get('release_date', '')
    category = input(f"Category [{item.get('category', '')}]: ").strip() or item.get('category', '')
    genre = input(f"Genre [{item.get('genre', '')}]: ").strip() or item.get('genre', '')

    updated_item = catalog.update_item(
        item_id, name, description, price, quantity, rating, platform, release_date, genre, category
    )
    if updated_item:
        print("Item updated:")
        print_item(updated_item)
    else:
        print("Failed to update item.")


# Delete an item
def delete_item():
    try:
        item_id = int(input("Enter the ID of the item to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a numeric value.")
        return

    item = catalog.get_item(item_id)
    if not item:
        print("Item not found.")
        return
    catalog.delete_item(item_id)
    print(f"Item with ID {item_id} deleted.")

# Search items by various fields
def search_items():
    print("\nSearch Options")
    print("1. Search by name")
    print("2. Search by description")
    print("3. Search by category")
    print("4. Search by genre")
    print("5. Search by platform")
    print("6. Search by release date")
    print("7. Search by rating")
    print("8. Back to main menu")
    choice = input("Choose an option: ").strip()

    results = []

    if choice == "1":
        query = input("Enter name to search: ").strip()
        results = catalog.search_items(query, field="name")
    elif choice == "2":
        query = input("Enter description to search: ").strip()
        results = catalog.search_items(query, field="description")
    elif choice == "3":
        query = input("Enter category to search: ").strip()
        results = catalog.search_items(query, field="category")
    elif choice == "4":
        query = input("Enter genre to search: ").strip()
        results = catalog.search_items(query, field="genre")
    elif choice == "5":
        query = input("Enter platform to search: ").strip()
        results = catalog.search_items(query, field="platform")
    elif choice == "6":
        query = input("Enter release date (YYYY-MM-DD) to search: ").strip()
        results = catalog.search_items(query, field="release_date")
    elif choice == "7":
        rating_input = input("Enter minimum rating to search: ").strip()
        results = catalog.search_by_rating_range(rating_input)
    elif choice == "8":
        query = input("Enter price range (min-max) to search: ").strip()
        results = catalog.search_by_price_range(query, field="price")
    elif choice == "9":
        return
    else:
        print("Invalid choice. Please try again.")
        return

    if not results:
        print("No items found.")
    else:
        print(f"Found {len(results)} items:")
        for item in results:
            print_item(item)

# 

# Main CLI loop
def main():
    while True:
        print("\nCatalog CLI")
        print("1. List all items")
        print("2. Add new item")
        print("3. Update item")
        print("4. Delete item")
        print("5. Search items")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            search_items()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

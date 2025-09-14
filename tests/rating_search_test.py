catalog = [
    {"id": 1, "name": "Game A", "rating": 4.49},
    {"id": 2, "name": "Game B", "rating": 3.2},
    {"id": 3, "name": "Game C", "rating": 2.75},
    {"id": 4, "name": "Game D", "rating": 4.0},
    {"id": 5, "name": "Game E", "rating": 1.5},
    {"id": 6, "name": "Game F", "rating": 0.9},
]

def search_by_rating_range(rating_input):
    global catalog

    try:
        if "-" in rating_input:
            min_rating, max_rating = map(float, rating_input.split("-"))
        else:
            center = float(rating_input)
            min_rating = max(center - 0.5, 0.0)
            max_rating = min(center + 0.49, 5.0)
    except ValueError:
        print("[DEBUG] Invalid rating input.")
        return []

    results = []
    for item in catalog:
        try:
            rating = float(item.get("rating", 0))
        except (ValueError, TypeError):
            continue

        if min_rating <= rating <= max_rating:
            results.append(item)

    print(f"[DEBUG] Searching for ratings between {min_rating} and {max_rating}. Found {len(results)} items.")
    return results


def test():
    tests = ["4", "3.5", "2-4", "5", "0", "invalid", "1.0", "3-3.5"]

    for test_input in tests:
        print(f"\nTest input: '{test_input}'")
        results = search_by_rating_range(test_input)
        for item in results:
            print(f"  - {item['name']} (rating: {item['rating']})")

if __name__ == "__main__":
    test()

# flask run --port=5050
    
from rating_search_test import search_by_rating_range  # Update import as needed

def test_search_by_rating_range_exact():
    result = search_by_rating_range("4")
    assert any(item["name"] == "Game A" for item in result)
    assert any(item["name"] == "Game D" for item in result)

from ccbake import Recipe

def test_recipe():
    # Explicit one-state recipe should stay as a one-element list
    one_item_list = Recipe('[{"op":"from morse code", "args": {"wordDelimiter": "Colon"}}]')
    assert len(one_item_list) == 1

    # Single stage recipe should become a one-element list
    one_item = Recipe('{"op":"from morse code", "args": {"wordDelimiter": "Colon"}}')
    assert len(one_item) == 1

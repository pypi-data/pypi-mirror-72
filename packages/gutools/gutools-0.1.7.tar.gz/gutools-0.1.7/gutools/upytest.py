import pytest


@pytest.fixture
def tempfolder():
    import tempfile
    with tempfile.TemporaryDirectory() as root:
        yield root


def select_one(elements):
    """*Select the 1st element and full key of an tree-dict struture.*
    
    """
    keys = []
    while isinstance(elements, dict):
        last_element = elements
        for key, elements in elements.items():
            if isinstance(elements, dict):
                keys.append(key)
            break
    return keys, last_element


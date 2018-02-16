from snactor import loader

def test_augeas():
    data = {}
    loader.get_actor("augeas").execute(data)
    assert bool(data) == True

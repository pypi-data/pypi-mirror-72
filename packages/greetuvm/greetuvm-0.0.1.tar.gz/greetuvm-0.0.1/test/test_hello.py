from hello import say_hello


def test_hello_no_params():
    assert say_hello() == 'Hello'


def test_hello_empty_param():
    assert say_hello('') == 'Hello'


def test_hello_abel():
    assert say_hello('Abel') == 'Hello, Abel'

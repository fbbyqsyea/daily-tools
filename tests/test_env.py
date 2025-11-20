from bbdtls import load_env, get_env, set_env

def test_load_and_get_env():
    load_env()
    assert get_env("PORT", 8888) == "8000"

def test_set_env():
    set_env("TEST_VAR", "123456")
    assert get_env("TEST_VAR", "default") == "123456"
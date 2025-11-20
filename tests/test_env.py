from bbdtls import Env


def test_env():
    env = Env('./.env.test')
    # 测试读取环境变量
    assert env.get_int("PORT", 8888) == 8000
    # 测试读取不存在的环境变量
    assert env.get("TEST_VAR", "default") == "default"

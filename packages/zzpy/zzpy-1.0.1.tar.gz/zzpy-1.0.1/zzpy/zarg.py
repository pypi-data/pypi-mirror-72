def get_env(key, default=None):
    """获取环境变量"""
    import os
    return os.environ.get(key, default)


def get_param(key, default=None, config_path='./config.json'):
    """优先从环境变量中获取，若不存在则从配置文件中获取，否则返回默认值"""
    value = get_env(key)
    if value:
        return value
    try:
        with open(config_path, encoding='utf8') as fr:
            import json
            params = json.loads(fr.read())
            value = params.get(key)
            if value:
                return value
    except Exception as ex:
        pass
    return default

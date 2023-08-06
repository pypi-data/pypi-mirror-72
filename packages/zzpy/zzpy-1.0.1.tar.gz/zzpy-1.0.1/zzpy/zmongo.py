def parse_mongo_url(mongo_url):
    import re
    host, port, database, param = re.search(
        r'^mongodb://(.*?):(\d*)/*([^\?]*)\?*(.*?)$', mongo_url).groups()
    if not host:
        host = 'localhost'

    if not port:
        port = 27017
    port = int(port)

    if param:
        param = dict([it.split('=') for it in param.split('&')])

    return host, port, database, param


def mongo_connect(mongo_url=None):
    def get_url_from_params():
        try:
            from .zarg import get_param
            return get_param("MONGO_URL")
        except:
            return None
    if not mongo_url:
        mongo_url = get_url_from_params()
    from pymongo import MongoClient
    import pytz
    host, port, database, _ = parse_mongo_url(mongo_url)
    client = MongoClient(host=host, port=port, tz_aware=True, tzinfo=pytz.timezone(
        'Asia/Shanghai')).get_database(database)
    return client


def main():
    pass


if __name__ == '__main__':
    main()

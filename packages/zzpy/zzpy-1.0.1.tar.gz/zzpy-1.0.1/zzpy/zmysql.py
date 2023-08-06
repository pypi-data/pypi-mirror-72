class MySQLClient:
    def __init__(self, mysql_url):
        self.client = self.new_mysql_client(mysql_url)

    @classmethod
    def new_mysql_client(cls, mysql_url):
        import pymysql
        host, port, database, user, password = cls.parse_mysql_url(mysql_url)
        client = pymysql.Connect(
            host=host, port=port, database=database, user=user, password=password)
        client.autocommit(True)
        return client

    @classmethod
    def parse_mysql_url(cls, mysql_url):
        import re
        host, port, database, param = re.search(
            r'^mysql://(.*?):(.*?)/(.*?)\?(.*?)$', mysql_url).groups()

        if not host:
            host = 'localhost'

        if not port:
            port = 3306
        port = int(port)

        user, password = None, None

        if param:
            param = dict([it.split('=') for it in param.split('&')])
            user = param['user']
            password = param['password']

        return host, port, database, user, password

    def scursor(self):
        from pymysql.cursors import SSCursor
        return SSCursor(self.client)

    def execute(self, sql):
        cursor = self.client.cursor()
        return cursor.execute(sql)

    def insert(self, sql):
        cursor = self.client.cursor()
        res = cursor.execute(sql)
        return cursor.lastrowid if res else 0

    def query(self, sql):
        cursor = self.client.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def query_one_value(self, sql):
        return self.query(sql)[0][0]

    def batch_insert(self, sql, values):
        """
        批量插入
        :param values: 插入的值
        :param sql: SQL
        :return:
        """
        cursor = self.client.cursor()
        row = cursor.executemany(sql, values)
        return cursor.lastrowid if row else 0


def mysql_connect(url=None):
    def get_url_from_params():
        try:
            from .zarg import get_param
            return get_param("MYSQL_URL")
        except:
            return None
    if not url:
        url = get_url_from_params()
    assert url
    return MySQLClient(url)

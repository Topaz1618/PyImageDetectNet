import tornado.ioloop
import tornado.web
import tornado.websocket


class Session:
    def __init__(self, session_id):
        self.session_id = session_id
        self.connections = set()

    def add_connection(self, connection):
        # 将连接添加到会话的连接集合中
        self.connections.add(connection)

    def remove_connection(self, connection):
        # 从会话的连接集合中移除连接
        self.connections.remove(connection)

    def handle_message(self, message):
        # 处理收到的消息，例如将消息发送给同一会话的其他连接
        for connection in self.connections:
            if connection != self:
                connection.write_message(message)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    # 哈希表用于存储会话对象
    sessions = {}

    def get_or_create_session(self, session_id):
        # 根据会话ID从哈希表中获取或创建会话对象
        if session_id in self.sessions:
            return self.sessions[session_id]
        else:
            session = Session(session_id)
            self.sessions[session_id] = session
            return session

    def get_session(self):
        # 根据连接获取关联的会话对象
        for session in self.sessions.values():
            if self in session.connections:
                return session
        return None

    def open(self, session_id):
        # 根据会话ID从哈希表中获取或创建会话对象
        session = self.get_or_create_session(session_id)
        # 关联会话对象与连接
        session.add_connection(self)

    def on_message(self, message):
        # 处理收到的消息
        # 使用会话对象进行处理，例如将消息发送给同一会话的其他连接等
        session = self.get_session()
        if session:
            session.handle_message(message)

    def on_close(self):
        # 在连接关闭时处理会话对象和连接的清理
        session = self.get_session()
        if session:
            session.remove_connection(self)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # 返回包含CSS和JavaScript的HTML页面
        self.render("index.html")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/ws/([^/]+)", WebSocketHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
#-*- coding:utf-8 -*-
import tornado.web
import tornado.websocket
import tornado.template
import tornado.ioloop
import tornado.gen
import camera
import time
import os


PORT = 8181
HOST = "127.0.0.1"

class HTTPHandler(tornado.web.RequestHandler):
    
    
    def get(self):
        loader = tornado.template.Loader('.')
        self.write(loader.load("index.html").generate(host=HOST, port=PORT))


class WebSocketsHandler(tornado.websocket.WebSocketHandler):
    
    
    def initialize(self):
        pass
    
    def check_origin(self, origin):
        return True
    
    @tornado.gen.coroutine
    def open(self):
        print("socket opened")
        self.camera = camera.Camera()
        yield self.video_loop()

    
    def on_message(self, message):
        print("recv: " + str(len(message)) + "symbols")
        self.write_message("Your message is '" + message +"'" + ", isn't it?")
    
    def on_close(self):
        print("socket closed")
        self.camera.destroy()
    
    @tornado.gen.coroutine
    def video_loop(self):
        while(True):
            try:
                self.write_message(self.camera.get_encode_frame())
                yield tornado.gen.Task(tornado.ioloop.IOLoop.current().add_timeout, time.time() + 0.0005)
            except Exception as e:
                break


if __name__ == "__main__":
    
    settings = {"static_path": os.path.join(os.path.dirname(__file__), "static")}
    app = tornado.web.Application([
        (r"/", HTTPHandler),
        (r"/ws", WebSocketsHandler),
        (r"/(websockets\.js)", tornado.web.StaticFileHandler, dict(path=settings['static_path']+"/js")),
        (r"/(video-stream\.css)", tornado.web.StaticFileHandler, dict(path=settings['static_path']+"/css"))
         ], **settings)
    app.listen(PORT)
    main_loop = tornado.ioloop.IOLoop.instance()
    main_loop.start()
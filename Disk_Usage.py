import os 
import shutil

from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Assignment(ServiceBase):
    @rpc(_returns=Iterable(Unicode))
    def Disk_space(self):
        total, used, free = shutil.disk_usage("/")
        yield u'Total: %d GB' % (total // (2**30))
        yield u'Used: %d GB' % (used // (2**30))
        yield u'Free: %d GB' %(free // (2**30))


application = Application([Assignment], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()

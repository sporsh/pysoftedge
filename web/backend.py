import os
import webbrowser

from twisted.internet import reactor
from twisted.web.server import Site, NOT_DONE_YET
from twisted.web import resource, static
from twisted.internet.protocol import ProcessProtocol

IPC_FD = 4 # fd to use for passing render data
SCENE_FILENAME = 'scene.pickle'


class RenderProcess(ProcessProtocol):
    def __init__(self, request):
        self.request = request
        self.abort = request.notifyFinish()
        self.abort.addErrback(self.terminate)
        self.data = []

    def childDataReceived(self, childFD, data):
        if childFD == IPC_FD:
            self.data.append(data)
#             self.request.write(data)

    def processEnded(self, reason):
        if not self.abort.called:
            self.request.write(''.join(self.data))
            self.request.finish()

    def terminate(self, reason):
        print "Terminating render process:", reason.value
        self.transport.signalProcess('KILL')


class RenderResource(resource.Resource):
    def render_GET(self, request):
        args = ['/usr/bin/pypy',
                '-m',
                "scripts.render_region",
                SCENE_FILENAME,
                str(IPC_FD),
                request.args['sx'][0],
                request.args['sy'][0],
                request.args['sw'][0],
                request.args['sh'][0]]
        reactor.spawnProcess(RenderProcess(request), args[0], args, env=os.environ,
                             childFDs={1:1, 2:2, 3:3, IPC_FD:'r'})
        return NOT_DONE_YET


if __name__ == '__main__':
#     from scripts.create_scene import save_scene
#     save_scene(SCENE_FILENAME)

    root = static.File('web/static')
    root.putChild('render', RenderResource())

    port = reactor.listenTCP(0, Site(root)).getHost().port
    reactor.callWhenRunning(webbrowser.open_new, 'http://localhost:%i' % port)
    reactor.run()

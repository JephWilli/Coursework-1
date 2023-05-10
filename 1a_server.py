import Pyro4
import os


# Define the remote object interface
@Pyro4.expose # Exposes the class and its methods to remote object via Pyro4
class FileServer(object):
    def get_file(self, filename):
        # Opens specified file, reads its contents, runs the commands in that indent
        with open(filename, 'rb') as f:
            contents = f.read()            
        return contents

# Start the Pyro4 daemon and register the remote object
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(FileServer)
ns.register('fileserver', uri)

print('File server ready.')
daemon.requestLoop()

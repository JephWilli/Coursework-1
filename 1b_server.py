import Pyro4
import os
import rsa
import base64

# Define the remote object interface
@Pyro4.expose # Exposes the class and its methods to remote object via Pyro4
class FileServer(object):
    def get_file(self, filename, private_key_contents):
        # Opens specified file, reads its contents, runs the commands in that indent
        with open(filename, 'rb') as f:
            contents = f.read()
            # Loads the public key from the specified file
            with open("public.pem", "rb") as f:
                public_key = rsa.PublicKey.load_pkcs1(f.read())
            # Encypts the file content using the public key and saves the encrypted message   
            encrypted_message = rsa.encrypt(contents, public_key)
            with open("encrypted.message", "wb") as f:
                f.write(encrypted_message)
                
            # Load the client's private key
            private_key = rsa.PrivateKey.load_pkcs1(private_key_contents.encode())
            # Use private key to decrypt the encrypted message
            decrypted_message = rsa.decrypt(encrypted_message, private_key)
        return [decrypted_message, encrypted_message]


# Start the Pyro4 daemon and register the remote object
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(FileServer)
ns.register('fileserver', uri)


print('File server ready.')
# Keeps the server running until its terminated
daemon.requestLoop()

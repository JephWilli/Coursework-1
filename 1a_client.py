import Pyro4
import base64

# Locate the Pyro4 nameserver and retrieve the remote object using the lookup method
ns = Pyro4.locateNS()
uri = ns.lookup('fileserver')

# Prompt for user to enter the file name
filename = input("Enter the filename to retrieve: ")

# Pryo4 proxy object is created using the uri
file_server = Pyro4.Proxy(uri)

# File contents are retrived from the server 
contents = file_server.get_file(filename)

# If the file content is not empty 
if contents is not None:
    # Print text found in file
    content_bytes = base64.b64decode(contents['data'])
    content_str = content_bytes.decode()
    print("Contents of file '{}':".format(filename))
    print(content_str)

# If file content is empty
else:
    print("Error: File '{}' not found on the server.".format(filename))




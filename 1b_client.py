import base64
import Pyro4

# List of encodings to try when decoding file contents
encodings = ['utf-8', 'iso-8859-1', 'ascii']

# Locate the Pyro4 nameserver and retrieve the remote object using the lookup method
ns = Pyro4.locateNS()
uri = ns.lookup('fileserver')

# Prompt for user to enter the file name and name of private key file for decryption
filename = input("Enter the filename to retrieve: ")
private_key = input("Enter the name of the private key file for decryption: ")

# Private key file is opened
with open(private_key, 'rb') as f:
    private_key_contents = f.read()
    # Its contents are read and decoded using the encodings listed
    for encoding in encodings:
        try:
            private_key_contents = private_key_contents.decode(encoding)
            break
        except UnicodeDecodeError:
            pass
    else:
        print("Error: Unable to decode file contents with any of the specified encodings.")


# Pryo4 proxy object is created using the uri
file_server = Pyro4.Proxy(uri)

# File contents are retrived from the server 
decrypted_message, encrypted_message = file_server.get_file(filename, private_key_contents)

# If the file content is not empty 
if (decrypted_message, encrypted_message)is not None:
    # Fetching the contents from its dictionary to its prefered data type
    encrypted_data = encrypted_message['data']  
    content_bytes = base64.b64decode(encrypted_data)

    decrypted_data = decrypted_message['data']
    decrypted_encoding = decrypted_message['encoding']
    decrypt_bytes = base64.b64decode(decrypted_data)

# Try decoding the content using different encodings until one works
    encodings = ["utf-8", "ascii", "iso-8859-1"]
    for encoding in encodings:
        try:
            decrypted_message = decrypt_bytes.decode(encoding)
            content_str = content_bytes.decode(encoding)
            # Print the decrypted and decrypted messages
            print(" ")
            print("Decrypted message:")
            print(decrypted_message)
            print(" ")
            print("Encrypted message:")
            print(content_str)
            break
        except UnicodeDecodeError:
            pass
    else:
        raise ValueError("Unable to decode file contents with any of the specified encodings.")

# If file content is empty
else:
    print("Error: File '{}' not found on the server.".format(filename))





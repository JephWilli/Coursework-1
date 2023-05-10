import rsa

# Generate a keypair using the RSA algorithm
public_key, private_key = rsa.newkeys(2048)

# Stores the key in specified location
with open("public.pem", "wb") as f:
    f.write(public_key.save_pkcs1("PEM"))
with open("private.pem", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))
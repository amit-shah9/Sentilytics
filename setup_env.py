import os
import certifi

# Set SSL cert path before any request-related libraries load
os.environ["SSL_CERT_FILE"] = certifi.where()

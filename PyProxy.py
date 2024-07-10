# Install: pip install mitmproxy
# Run: mitmdump -s PyProxy.py --listen-host <interface> --listen-port <port>

import os
import subprocess
import json
import datetime
import base64

def ensure_cert_exists():
    cert_file = "mitmproxy-ca-cert.crt"
    if not os.path.isfile(cert_file):
        # Bash script to copy the certificate
        bash_script = f"""
        #!/bin/bash
        SOURCE_DIR="$HOME/.mitmproxy"
        CERT_FILE="mitmproxy-ca-cert.pem"
        DEST_DIR=$(pwd)
        DEST_CERT_FILE="mitmproxy-ca-cert.crt"

        # Check if the certificate file exists in the source directory
        if [ -f "$SOURCE_DIR/$CERT_FILE" ]; then
          # Copy and rename the certificate file to the current directory
          cp "$SOURCE_DIR/$CERT_FILE" "$DEST_DIR/$DEST_CERT_FILE"
          echo "Certificate copied to $DEST_DIR/$DEST_CERT_FILE"
        else
          echo "Certificate file not found in $SOURCE_DIR"
        fi
        """

        # Execute the bash script
        process = subprocess.Popen(bash_script, shell=True, executable='/bin/bash')
        process.communicate()
    else:
        print(f"Certificate already exists in the current directory: {cert_file}")

def ensure_request_response_dir():
    base_dir = "HTTP"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return base_dir

# Ensure the certificate exists
ensure_cert_exists()

# Ensure the RequestResponse directory exists
base_dir = ensure_request_response_dir()

from mitmproxy import http
from mitmproxy import ctx

class Logger:
    def __init__(self):
        self.num = 0
        self.current_requests = {}

    def request(self, flow: http.HTTPFlow) -> None:
        self.num += 1
        request_log = {
            "num": self.num,
            "timestamp": str(datetime.datetime.now()),
            "request": {
                "method": flow.request.method,
                "url": flow.request.url,
                "headers": dict(flow.request.headers),
                "content": base64.b64encode(flow.request.content).decode('utf-8')
            }
        }
        self.current_requests[flow.id] = request_log

    def response(self, flow: http.HTTPFlow) -> None:
        request_log = self.current_requests.pop(flow.id, None)
        if request_log:
            response_log = {
                "num": self.num,
                "timestamp": str(datetime.datetime.now()),
                "response": {
                    "status_code": flow.response.status_code,
                    "headers": dict(flow.response.headers),
                    "content": base64.b64encode(flow.response.content).decode('utf-8')
                }
            }
            combined_log = {**request_log, **response_log}
            self.save_combined_log(combined_log, flow)

    def save_combined_log(self, log_data, flow):
        content_length = len(json.dumps(log_data))
        file_size_kb = round(content_length / 1024)
        file_name = f"{self.num}_{flow.request.method}_{file_size_kb}k.json"
        file_path = os.path.join(base_dir, file_name)
        with open(file_path, "w") as f:
            json.dump(log_data, f, indent=4)
        ctx.log.info(f"Saved combined log to {file_path}")

addons = [
    Logger()
]

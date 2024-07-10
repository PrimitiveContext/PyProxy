
## PyProxy

A Python `mitmproxy` wrapper to proxy and save HTTP request/response data.
- **Browser Certificate:** Auto-generated and placed in the working directory.
- **Request/Response:** Each pair stored together, labeled with size in KB.
- **Switches:** Host. Port. (*:8080 default)

### Installation

```bash
pip install mitmproxy
```

### Usage

```bash
mitmdump -s PyProxy.py --listen-host <interface> --listen-port <port>
```

### Output (example)
```
└─$ tree                           
.
├── HTTP
│   ├── 10_GET_9k.json
│   ├── 1_POST_14k.json
│   ├── 2_POST_3k.json
│   ├── 3_POST_2k.json
│   ├── 4_POST_17k.json
│   ├── 5_POST_3k.json
│   ├── 6_POST_9k.json
│   ├── 7_POST_17k.json
│   ├── 8_POST_14k.json
│   └── 9_GET_1k.json
├── mitmproxy-ca-cert.crt
└── PyProxy.py

2 directories, 12 files
```

### Requirements

- mitmproxy
- Python 3.x
- Bash (for certificate management)

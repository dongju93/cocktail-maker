import os
from multiprocessing import cpu_count

from dotenv import load_dotenv

load_dotenv()

##### Server Socket #####
bind = "0.0.0.0:8000"
backlog = 2048  # Handle connection bursts

##### Worker Processes #####
# Use Uvicorn worker for async frameworks like FastAPI
worker_class = "uvicorn_worker.UvicornWorker"
# Max simultaneous clients
worker_connections = 1000

##### Worker Lifecycle & Stability #####
# Restart workers after this many requests to prevent memory leaks
max_requests = 1000
# Add random jitter to max_requests to prevent all workers restarting at once
max_requests_jitter = 100
# Use shared memory for worker temp files (Linux only)
# worker_tmp_dir = "/dev/shm"
# Abort workers that hit a memory error
worker_abort_on_memory_error = True

##### Timeouts #####
# Increased for long operations like file uploads
timeout = 90
# Time for graceful shutdown
graceful_timeout = 30
# Keepalive connection duration
keepalive = 2

##### Security #####
# Mitigate buffer overflow attacks
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8192
# Trust proxy headers (adjust "*" in production for specific IPs)
forwarded_allow_ips = "*"

##### Logging #####
accesslog = "-"  # Log to stdout
errorlog = "-"  # Log to stderr
# More precise response time logging (microseconds)
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

##### Process Naming #####
proc_name = "cocktail_maker"

##### Application #####
# Preload app code before forking workers for better memory usage & faster boot
preload_app = True

##### Performance Optimization #####
# Enable SO_REUSEPORT for better load balancing (Linux/macOS)
reuse_port = True
# Disable access log buffering for real-time logs
disable_redirect_access_to_syslog = True

##### Environment-specific Overrides #####
ENVIRONMENT = os.getenv("ENVIRONMENT", "production").lower()

if ENVIRONMENT == "development":
    # Dev settings: single worker, debug logging, autoreload
    workers = 1
    loglevel = "debug"
    reload = True
    # Faster timeout for development
    timeout = 60
    # Enable detailed error reporting
    capture_output = False
elif ENVIRONMENT == "production":
    # Production settings: optimized worker count
    cpu_cores = cpu_count()
    workers = min(
        cpu_cores * 2 + 1, 8
    )  # Cap at 8 workers for better resource management
    loglevel = os.getenv("LOG_LEVEL", "info").lower()
    reload = False
    # Production timeout
    timeout = 90
    # Capture output for better logging
    capture_output = True

    # Memory optimization for production
    max_requests = 800
    max_requests_jitter = 80

    # Enable sendfile for static files (if serving any)
    # sendfile = True # nginx handles
    # Optimize for production logging
    access_log_format = '%(h)s "%(r)s" %(s)s %(b)s %(D)s'

# SSL Configuration (uncomment and configure if needed)
# keyfile = os.getenv("SSL_KEYFILE", "/path/to/key.pem")
# certfile = os.getenv("SSL_CERTFILE", "/path/to/cert.pem")
# ssl_version = ssl.PROTOCOL_TLS
# cert_reqs = ssl.CERT_NONE
# ca_certs = None
# suppress_ragged_eofs = True
# do_handshake_on_connect = False
# ciphers = "ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS"

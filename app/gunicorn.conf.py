from multiprocessing import cpu_count

bind = "0.0.0.0:8000"  # Use default port
workers = cpu_count() * 2 + 1  # Recommended
worker_class = "uvicorn_worker.UvicornWorker"
max_requests = 1000  # Restart workers for preventing memory leaks
max_requests_jitter = (
    50  # Individual workers will be restarted with a this random delay
)
accesslog = "-"  # stdout for access log
errorlog = "-"
timeout = 60  # Worker timeout in seconds
preload_app = (
    True  # Process the application code before the worker processes are forked
)
proc_name = "cocktail_maker"  # Process name

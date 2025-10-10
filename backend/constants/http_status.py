"""
HTTP status codes constants.
Eliminates magic numbers in HTTP responses.
"""

class HTTPStatusCodes:
    """Standard HTTP status codes used in the application."""
    
    # Success codes (2xx)
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    
    # Redirection codes (3xx)
    MOVED_PERMANENTLY = 301
    FOUND = 302
    NOT_MODIFIED = 304
    
    # Client error codes (4xx)
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    TOO_MANY_REQUESTS = 429
    
    # Server error codes (5xx)
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508


class HTTPStatusMessages:
    """Human-readable messages for HTTP status codes."""
    
    # Success messages
    OK = "Request successful"
    CREATED = "Resource created successfully"
    ACCEPTED = "Request accepted for processing"
    NO_CONTENT = "Request successful, no content to return"
    
    # Client error messages
    BAD_REQUEST = "Bad request"
    UNAUTHORIZED = "Authentication required"
    FORBIDDEN = "Access forbidden"
    NOT_FOUND = "Resource not found"
    METHOD_NOT_ALLOWED = "HTTP method not allowed"
    REQUEST_TIMEOUT = "Request timeout"
    CONFLICT = "Resource conflict"
    PAYLOAD_TOO_LARGE = "Request payload too large"
    UNSUPPORTED_MEDIA_TYPE = "Unsupported media type"
    UNPROCESSABLE_ENTITY = "Request data validation failed"
    TOO_MANY_REQUESTS = "Rate limit exceeded"
    
    # Server error messages
    INTERNAL_SERVER_ERROR = "Internal server error"
    NOT_IMPLEMENTED = "Feature not implemented"
    BAD_GATEWAY = "Bad gateway"
    SERVICE_UNAVAILABLE = "Service temporarily unavailable"
    GATEWAY_TIMEOUT = "Gateway timeout"


# Common HTTP status code groups
SUCCESS_CODES = [
    HTTPStatusCodes.OK,
    HTTPStatusCodes.CREATED,
    HTTPStatusCodes.ACCEPTED,
    HTTPStatusCodes.NO_CONTENT
]

CLIENT_ERROR_CODES = [
    HTTPStatusCodes.BAD_REQUEST,
    HTTPStatusCodes.UNAUTHORIZED,
    HTTPStatusCodes.FORBIDDEN,
    HTTPStatusCodes.NOT_FOUND,
    HTTPStatusCodes.METHOD_NOT_ALLOWED,
    HTTPStatusCodes.UNPROCESSABLE_ENTITY,
    HTTPStatusCodes.TOO_MANY_REQUESTS
]

SERVER_ERROR_CODES = [
    HTTPStatusCodes.INTERNAL_SERVER_ERROR,
    HTTPStatusCodes.NOT_IMPLEMENTED,
    HTTPStatusCodes.BAD_GATEWAY,
    HTTPStatusCodes.SERVICE_UNAVAILABLE,
    HTTPStatusCodes.GATEWAY_TIMEOUT
]
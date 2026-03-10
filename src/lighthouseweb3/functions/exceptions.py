"""Custom exceptions for Lighthouse Web3 SDK."""


class LighthouseError(Exception):
    """Base exception class for all Lighthouse SDK errors."""

    pass


class LighthouseAPIError(LighthouseError):
    """Exception raised for HTTP/API errors from Lighthouse services."""

    pass


class LighthouseUploadError(LighthouseError):
    """Exception raised for upload-related errors."""

    pass

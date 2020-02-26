class DrandException(Exception):
    """Base class for drand exceptions."""


class VerificationFailure(DrandException):
    """Error raised when the verification for a random value fails.
    The random value is fetched from a node of a drand network.
    """


class SignatureVerificationFailure(VerificationFailure):
    """Error raised when the verification of the signature fails."""

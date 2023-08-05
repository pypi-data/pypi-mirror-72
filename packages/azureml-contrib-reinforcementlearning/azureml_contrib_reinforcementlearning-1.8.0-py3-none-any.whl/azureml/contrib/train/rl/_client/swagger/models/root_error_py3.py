# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from msrest.serialization import Model


class RootError(Model):
    """The root error.

    :param code: The service-defined error code. Supported error codes:
     ServiceError, UserError, ValidationError, AzureStorageError,
     TransientError, RequestThrottled.
    :type code: str
    :param message: A human-readable representation of the error.
    :type message: str
    :param target: The target of the error (e.g., the name of the property in
     error).
    :type target: str
    :param details: The related errors that occurred during the request.
    :type details: list[~reinforcementlearning.models.RootError]
    :param inner_error: A nested list of inner errors. When evaluating errors,
     clients MUST traverse through all of the nested "innerErrors" and choose
     the deepest one that they understand.
    :type inner_error: ~reinforcementlearning.models.InnerErrorResponse
    """

    _attribute_map = {
        'code': {'key': 'code', 'type': 'str'},
        'message': {'key': 'message', 'type': 'str'},
        'target': {'key': 'target', 'type': 'str'},
        'details': {'key': 'details', 'type': '[RootError]'},
        'inner_error': {'key': 'innerError', 'type': 'InnerErrorResponse'},
    }

    def __init__(self, *, code: str = None, message: str = None, target: str = None,
                 details=None, inner_error=None, **kwargs) -> None:
        super(RootError, self).__init__(**kwargs)
        self.code = code
        self.message = message
        self.target = target
        self.details = details
        self.inner_error = inner_error

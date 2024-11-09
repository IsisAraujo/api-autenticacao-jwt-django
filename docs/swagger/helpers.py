from .security import security_decorator


def create_protected_schema(description, request_body=None, responses=None):
    """Helper para criar schemas protegidos com JWT"""
    schema_kwargs = {"operation_description": description, **security_decorator}

    if request_body:
        schema_kwargs["request_body"] = request_body

    if responses:
        schema_kwargs["responses"] = {**security_decorator["responses"], **responses}

    return schema_kwargs

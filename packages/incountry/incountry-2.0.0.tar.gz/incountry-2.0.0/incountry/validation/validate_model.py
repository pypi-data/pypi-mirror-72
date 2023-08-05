from inspect import getfullargspec

import wrapt
from pydantic import ValidationError


from .utils import function_args_to_kwargs, get_formatted_validation_error
from ..exceptions import StorageException, StorageClientException, StorageServerException


def get_validated_data(function, model, **kwargs):
    try:
        return model.validate(kwargs).dict()
    except ValidationError as e:
        errors_report = get_formatted_validation_error(e)
        error_text = "Validation failed during {}():{}".format(function.__qualname__, errors_report)
        raise StorageClientException(error_text) from None


def validate_model(model):
    @wrapt.decorator
    def decorator(function, instance, args, kwargs):
        function_args_to_kwargs(function, args, kwargs)
        validated_data_dict = get_validated_data(function, model, **kwargs)
        func_args = getfullargspec(function)[0]

        for key in func_args:
            if key in validated_data_dict:
                kwargs[key] = validated_data_dict[key]
        try:
            return function(**kwargs)
        except StorageClientException as e:
            raise StorageClientException(f"Validation failed during {function.__qualname__}()") from e
        except StorageServerException as e:
            raise e
        except StorageException as e:
            raise e
        except Exception as e:
            raise StorageException(f"{e.__class__.__qualname__} during {function.__qualname__}()") from e

    return decorator

from typing import List, Union

# Interfaces
class IRequest:
    input_data: List[type]


class IColumns:
    name: str
    width: int = None  # Optional, defaults to None if not provided


class IParameters:
    name: str
    id: str
    type: str
    choices: List[str] = None  # Optional, defaults to None if not provided
    default: Union[str, int, float]  # Can be either string or integer or float
    read_only: bool = False


# Props
class InteractiveFeatureProps:
    example: List[dict]
    parameters: List[IParameters]
    input: List[IColumns]
    output: List[IColumns]


class MultiInteractiveFeatureProps:
    options: dict
    parameters: List[IParameters]


# Respond
class ApiResponse:
    result: List
    code: str

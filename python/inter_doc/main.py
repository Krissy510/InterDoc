from typing import Dict, List, get_type_hints
from .models import (ApiResponse, IRequest, IColumns, InteractiveFeatureProps,
                     IParameters, MultiInteractiveFeatureProps)


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class InterDocGen(metaclass=SingletonMeta):
    def __init__(self, FIELD_WIDTHS: dict, PRESET_PARAMETERS: dict):

        if len(FIELD_WIDTHS) == 0:
            raise KeyError('FIELD_WIDTHS is empty')

        if len(PRESET_PARAMETERS) == 0:
            raise KeyError('FIELD_WIDTHS is empty')

        self.__FIELDS_WIDTHS = FIELD_WIDTHS
        self.__PRESET_PARAMETERS = PRESET_PARAMETERS

    def get_current_fields_widths(self):
        return self.__FIELDS_WIDTHS

    def get_current_preset_para(self):
        return self.__PRESET_PARAMETERS

    def set_fields_widths(self, FIELD_WIDTHS: dict):
        self.__FIELDS_WIDTHS = FIELD_WIDTHS

    def set_preset_parameters(self, PRESET_PARAMETERS: dict):
        self.__PRESET_PARAMETERS = PRESET_PARAMETERS

    def generate_columns(self, cls: type) -> List[IColumns]:
        return [{'name': field_name, 'width': self.__FIELDS_WIDTHS[field_name]}
                for field_name in (get_type_hints(cls).keys())]

    def generate_parameters(self, cls: type) -> List[IParameters]:
        parameters = list(get_type_hints(cls).keys())
        parameters.remove('input_data')
        return [self.__PRESET_PARAMETERS[parameter] for parameter in parameters]

    def generate_interactive_props(self, example: List[dict],
                                   requestClass: IRequest,
                                   outputClass: type,
                                   ) -> InteractiveFeatureProps:
        type_hints = get_type_hints(requestClass)
        query_type = type_hints['input_data'].__args__[0]
        return {
            'example': example,
            'input_data': self.generate_columns(cls=query_type),
            'output': self.generate_columns(cls=outputClass),
            'parameters': self.generate_parameters(cls=requestClass)
        }

    def generate_multi_interactive_props(self,
                                         optionsName: List[str],
                                         defaultOption: str,
                                         examples: List[List[dict]],
                                         requestClasses: List[type],
                                         outputClasses: List[type],
                                         parameters: List[str]):
        options = dict()
        for i in range(len(requestClasses)):
            type_hints = get_type_hints(requestClasses[i])
            query_type = type_hints['input_data'].__args__[0]
            options[optionsName[i]] = {
                'example': examples[i],
                'input_data': self.generate_columns(query_type),
                'output': self.generate_columns(outputClasses[i]),
            }

        parameter = [self.__PRESET_PARAMETERS[parameter]
                     for parameter in parameters]
        parameter.append({
            'name': 'Type',
            'type': 'select',
            'default': defaultOption,
            'id': 'type',
            'choices': optionsName
        })
        return {
            'options': options,
            'parameters': parameter
        }

    def generate_api_response(self, result: List[type],
                              generated_code: str,
                              ) -> ApiResponse:
        return ({
            'result': result,
            'code': generated_code
        })

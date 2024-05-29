from inter_doc import InterDocGen, IRequest
import unittest
from typing import List

FIELD_WIDTHS = {
    'qid': 80,
    'query': 200,
    'score': 80,
}

PRESET_PARAMETERS = {
    'num_results': {
        'name': 'Num of result',
        'type': 'number',
        'default': 5,
        'id': 'num_results',
    },
    'length': {
        'name': 'Length',
        'type': 'number',
        'default': 5,
        'id': 'length',
    },
}


class TestInput():
    qid: str
    query: str


class TestRequest():
    input_data: List[TestInput]
    num_results: int
    length: int


class TestResult(TestInput):
    score: float


# Expected constant
EXPECTED_COLUMNS = [{'name': 'qid', 'width': FIELD_WIDTHS['qid']},
                    {'name': 'query', 'width': FIELD_WIDTHS['query']}]

EXPECTED_PARAMETERS = [{'name': 'Num of result', 'type': 'number', 'default': 5, 'id': 'num_results'},
                       {'name': 'Length', 'type': 'number', 'default': 5, 'id': 'length'}]

EXPECTED_OUTPUTS = [{'name': 'qid', 'width': FIELD_WIDTHS['qid']},
                    {'name': 'query', 'width': FIELD_WIDTHS['query']},
                    {'name': 'score', 'width': FIELD_WIDTHS['score']}]

EXPECTED_EXAMPLES = [{'qid': '0', 'query': 'how to retrieve text'},
                     {'qid': '1', 'query': 'what is an inverted index'}]

EXPECTED_INTER_PROPS = {
    'example': EXPECTED_EXAMPLES,
    'parameters': EXPECTED_PARAMETERS,
    'input_data': EXPECTED_COLUMNS,
    'output': EXPECTED_OUTPUTS
}

EXPECTED_RESULT = [{'qid': '0', 'query': 'how to retrieve text', 'score': 1.4},
                   {'qid': '1', 'query': 'what is an inverted index', 'score': 2.5}]

EXPECTED_GENERATED_CODE = "print('test code')"

EXPECTED_RESPONSE = {
    'result': EXPECTED_RESULT,
    'code': EXPECTED_GENERATED_CODE
}

EXPECTED_MULTI_EXAMPLES = [[{'qid': 0, 'query': 'smth'},{'qid': 1, 'query': 'smth_2'}],
                             [{'qid': 2, 'query': 'nothing'},{'qid': 3, 'query': 'nothing2'}]]

EXPECTED_MULTI_PARAMETERS = EXPECTED_PARAMETERS[:]
EXPECTED_MULTI_PARAMETERS.append({
    'name': 'Type',
    'type': 'select',
    'default': 'first',
    'id': 'type',
    'choices': ['first', 'second']
})

EXPECTED_MULTI_INTER_PROPS = {
    'options': {
        'first': {
            'example': EXPECTED_MULTI_EXAMPLES[0], 
            'input_data': EXPECTED_COLUMNS, 
            'output': EXPECTED_OUTPUTS
            }, 
        'second': {
            'example': EXPECTED_MULTI_EXAMPLES[1], 
            'input_data': EXPECTED_COLUMNS, 
            'output': EXPECTED_OUTPUTS
            }
    }, 
    'parameters': [
        {'name': 'Length', 'type': 'number', 'default': 5, 'id': 'length'}, 
        {'name': 'Num of result', 'type': 'number', 'default': 5, 'id': 'num_results'}, 
        {'name': 'Type', 'type': 'select', 'default': 'first', 'id': 'type', 'choices': ['first', 'second']}
        ]
}

inter_doc = InterDocGen(FIELD_WIDTHS, PRESET_PARAMETERS)

class TestGenerators(unittest.TestCase):
    def test_gen_cols(self):
        """
        Test that it can generate columns using class only
        """
        result = inter_doc.generate_columns(TestInput)
        self.assertEqual(result, EXPECTED_COLUMNS)

    def test_gen_paras(self):
        """
        Test that it can generate parameter using class only
        """
        result = inter_doc.generate_parameters(TestRequest)
        self.assertEqual(result, EXPECTED_PARAMETERS)

    def test_gen_interactive_props(self):
        """
        Test that it can generate interactive props using request and result class with example
        """
        result = inter_doc.generate_interactive_props(
            EXPECTED_EXAMPLES, TestRequest, TestResult)
        self.assertEqual(result, EXPECTED_INTER_PROPS)

    def test_gen_muli_interactive_props(self):
        """
        Test that it can generate multi interactive props using List of request, result, example, and parameter
        """
        options = ['first', 'second']
        parameters = ['length', 'num_results']

        result = inter_doc.generate_multi_interactive_props(
            optionsName=options,
            defaultOption=options[0],
            examples=EXPECTED_MULTI_EXAMPLES,
            requestClasses=[TestRequest, TestRequest],
            outputClasses=[TestResult, TestResult],
            parameters=parameters)
            
        self.assertEqual(result, EXPECTED_MULTI_INTER_PROPS)

    def test_gen_api_response(self):
        """
        Test if it creates API response using default parameters 
        """
        result = inter_doc.generate_api_response(
            EXPECTED_RESULT, EXPECTED_GENERATED_CODE)
        self.assertEqual(result, EXPECTED_RESPONSE)


if __name__ == '__main__':
    unittest.main()

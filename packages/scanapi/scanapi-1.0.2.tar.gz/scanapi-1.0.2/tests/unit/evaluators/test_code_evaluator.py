import os
import pytest
import requests

from scanapi.errors import BadConfigurationError, InvalidPythonCodeError
from scanapi.evaluators import CodeEvaluator, SpecEvaluator, StringEvaluator


class TestCodeEvaluator:
    class TestEvaluate:
        class TestWhenDoesNotMatchThePattern:
            test_data = ["no code", "${CODE}", "${code}", "{{code}}"]

            @pytest.mark.parametrize("sequence", test_data)
            def test_should_return_sequence(self, sequence):
                assert CodeEvaluator.evaluate(sequence, {}) == sequence

        class TestWhenMatchesThePattern:
            class TestWhenItIsATestCase:
                test_data = [
                    ("${{1 == 1}}", (True, None)),
                    ("${{1 == 4}}", (False, "1 == 4")),
                ]

                @pytest.mark.parametrize("sequence, expected", test_data)
                def test_should_return_assert_results(self, sequence, expected):
                    assert (
                        CodeEvaluator.evaluate(sequence, {}, is_a_test_case=True)
                        == expected
                    )

                class TestWhenCodeContainsPreSavedResponse:
                    @pytest.fixture
                    def response(self, requests_mock):
                        requests_mock.get("http://test.com", text="abcde")
                        return requests.get("http://test.com")

                    test_data = [
                        ("${{response.text == 'abcde'}}", (True, None)),
                        ("${{response.url == 'http://test.com/'}}", (True, None)),
                        (
                            "${{response.status_code == 300}}",
                            (False, "response.status_code == 300"),
                        ),
                        (
                            "${{response.url == 'abc'}}",
                            (False, "response.url == 'abc'"),
                        ),
                    ]

                    @pytest.mark.parametrize("sequence, expected", test_data)
                    def test_should_return_assert_results(
                        self, sequence, expected, response
                    ):
                        assert (
                            CodeEvaluator.evaluate(
                                sequence, {"response": response}, is_a_test_case=True
                            )
                            == expected
                        )

                class TestWhenCodeBreaks:
                    def test_should_raises_invalid_python_code_error(self):
                        with pytest.raises(InvalidPythonCodeError) as excinfo:
                            CodeEvaluator.evaluate(
                                "${{response.url == 'abc'}}", {}, is_a_test_case=True
                            )

                        assert (
                            str(excinfo.value)
                            == "Invalid Python code defined in the API spec. "
                            "Exception: 'NoneType' object has no attribute 'url'. "
                            "Code: response.url == 'abc'."
                        )

            class TestWhenItIsNotATestCase:
                test_data = [("${{1 + 1}}", "2"), ("${{'hi'*4}}", "hihihihi")]

                @pytest.mark.parametrize("sequence, expected", test_data)
                def test_should_return_evaluated_code(self, sequence, expected):
                    assert CodeEvaluator.evaluate(sequence, {}) == expected

                class TestWhenCodeContainsPreSavedResponse:
                    @pytest.fixture
                    def response(self, requests_mock):
                        requests_mock.get("http://test.com", text="abcde")
                        return requests.get("http://test.com")

                    test_data = [
                        ("${{response.text}}", "abcde"),
                        ("${{response.status_code}}", "200"),
                        ("${{response.text + 'xpto'}}", "abcdexpto"),
                        ("${{'xpto' + response.text}}", "xptoabcde"),
                        ("${{1+1}}", "2"),
                    ]

                    @pytest.mark.parametrize("sequence, expected", test_data)
                    def test_should_return_evaluated_code(
                        self, sequence, expected, response
                    ):
                        assert (
                            CodeEvaluator.evaluate(sequence, {"response": response})
                            == expected
                        )

                class TestWhenCodeBreaks:
                    def test_should_raises_invalid_python_code_error(self):
                        with pytest.raises(InvalidPythonCodeError) as excinfo:
                            CodeEvaluator.evaluate("${{1/0}}", {})

                        assert (
                            str(excinfo.value)
                            == "Invalid Python code defined in the API spec. "
                            "Exception: division by zero. Code: 1/0."
                        )

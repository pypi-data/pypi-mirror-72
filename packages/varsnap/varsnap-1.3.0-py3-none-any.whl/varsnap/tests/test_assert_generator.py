import os
import unittest
from unittest.mock import MagicMock, patch

from typing import Any, List

from varsnap import assert_generator, core


def add(x: int, y: int) -> int:
    return x + y


null = open(os.devnull, 'w')


class TestResult(unittest.runner.TextTestResult):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(TestResult, self).__init__(*args, **kwargs)
        self.successes: List[Any] = []

    def addSuccess(self, test: Any) -> None:
        super(TestResult, self).addSuccess(test)
        self.successes.append(test)


class TestTest(unittest.TestCase):
    def setUp(self) -> None:
        core.CONSUMERS = []

    def tearDown(self) -> None:
        core.CONSUMERS = []

    def test_no_consumers(self) -> None:
        all_matches, all_logs = assert_generator.test()
        self.assertEqual(all_matches, None)
        self.assertEqual(all_logs, "")

    @patch('varsnap.core.Consumer.consume')
    def test_consume(self, mock_consume: MagicMock) -> None:
        core.Consumer(add)
        trial = core.Trial(core.Inputs([1, 1], {}, {}), 2)
        trial.matches = True
        mock_consume.return_value = [trial]
        all_matches, all_logs = assert_generator.test()
        self.assertTrue(all_matches)
        self.assertEqual(all_logs, '')

    @patch('varsnap.core.Consumer.consume')
    def test_consume_fail(self, mock_consume: MagicMock) -> None:
        core.Consumer(add)
        trial = core.Trial(core.Inputs([1, 1], {}, {}), 2)
        trial.matches = False
        trial.report = 'abcd'
        mock_consume.return_value = [trial]
        all_matches, all_logs = assert_generator.test()
        self.assertFalse(all_matches)
        self.assertEqual(all_logs, 'abcd')

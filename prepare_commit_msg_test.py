# Copyright 2023 EATING-OUT Ltd.


import re
import unittest


def replace_title_with_codegpt_title(
    codegpt_commit_title: str, prev_commit_msg: str
) -> str:
    pattern = r"\s-\s.*"
    replace = f" - {codegpt_commit_title}"
    return re.sub(pattern, replace, prev_commit_msg, count=1)


class TestReplaceTitleWithCodegptTitle(unittest.TestCase):
    def test_replace_title_with_codegpt_title(self):
        testCases = [
            [
                """
[repo-name] #123 - old title

- feat: add new feature

Reviewer: reviewer
                """,
                "new title",
                """
[repo-name] #123 - new title

- feat: add new feature

Reviewer: reviewer
                """,
            ],
            [
                """
[repo-name] #123 - old title (codegen)

- feat: add new feature

Reviewer: reviewer
                """,
                "new title",
                """
[repo-name] #123 - new title

- feat: add new feature

Reviewer: reviewer
                """,
            ],
        ]

        for prev_commit_msg, codegpt_commit_title, expect_result_msg in testCases:
            actual_result_msg = replace_title_with_codegpt_title(
                codegpt_commit_title, prev_commit_msg
            )
            self.assertEqual(expect_result_msg, actual_result_msg)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-

from unittest import TestCase
from accarbon_command.accarbon import get_soup
from accarbon_command.atcoder import url_validation, get_submission_id, get_submission_code, get_submission_info, get_contest_title, get_tweet_title


class TestAtCoder(TestCase):
    def test_url_validation(self):
        test_patterns = [
            ('https://atcoder.jp/contests/abc170/submissions/14465204', True),
            ('https://atcoder.jp/contests/abc170/submissions/14465204?lang=ja', True),
            ('https://atcoder.jp/contests/abc170/submissions/14465204?lang=en', True),
            ('https://atcoder.jp/contests/abc170/submissions/14465204?lang=ko', False),
            ('http://atcoder.jp/contests/abc170/submissions/14465204', False),
            ('https://atcoder.jp/contests/abc170/submissions/xxxxxxxx', False),
        ]
        for url, ans in test_patterns:
            with self.subTest(url=url, ans=ans):
                self.assertEqual(url_validation(url), ans)

    def test_get_submission_id(self):
        test_patterns = [
            ('https://atcoder.jp/contests/abc170/submissions/14465204', '14465204'),
            ('https://atcoder.jp/contests/abc170/submissions/14465204?lang=ja', '14465204'),
            ('https://atcoder.jp/contests/abc170/submissions/14465204?lang=en', '14465204'),
        ]
        for url, ans in test_patterns:
            with self.subTest(url=url, ans=ans):
                self.assertEqual(get_submission_id(url), ans)

    def test_get_submission_code(self):
        test_patterns = [
            ('https://atcoder.jp/contests/abc170/submissions/14465204', '''#include <bits/stdc++.h>\r
using namespace std;\r
#define rep(i, n) for (int i = 0, i##_cond = (n); i < i##_cond; ++i)\r
\r
int main() {\r
  rep(i, 5) {\r
    int a;\r
    cin >> a;\r
    if (a == 0)\r
      cout << i + 1 << endl;\r
  }\r
}'''),
        ]
        for url, ans in test_patterns:
            with self.subTest(url=url, ans=ans):
                self.assertEqual(get_submission_code(get_soup(url), url), ans)

    def test_get_submission_info(self):
        test_patterns = [
            # C++ (GCC 9.2.1), AC
            (
                'https://atcoder.jp/contests/abc170/submissions/14465204',
                {
                    'problem': 'A - Five Variables',
                    'user': 'kimitsu_emt ',
                    'lang': 'C++ (GCC 9.2.1)',
                    'length': '229 Byte',
                    'result': 'AC',
                    'time': '6 ms'
                }
            ),
            # WA
            (
                'https://atcoder.jp/contests/abc170/submissions/14351771',
                {
                    'problem': 'F - Pond Skater',
                    'user': 'kimitsu_emt ',
                    'lang': 'C++ (GCC 9.2.1)',
                    'length': '1884 Byte',
                    'result': 'WA',
                    'time': '64 ms'
                }
            ),
            # TLE
            (
                'https://atcoder.jp/contests/abc170/submissions/14350983',
                {
                    'problem': 'F - Pond Skater',
                    'user': 'kimitsu_emt ',
                    'lang': 'C++ (GCC 9.2.1)',
                    'length': '1864 Byte',
                    'result': 'TLE',
                    'time': '3308 ms'
                }
            ),
            # C (GCC 9.2.1)
            (
                'https://atcoder.jp/contests/abc170/submissions/14386050',
                {
                    'problem': 'A - Five Variables',
                    'user': 'Shiro_S ',
                    'lang': 'C (GCC 9.2.1)',
                    'length': '56 Byte',
                    'result': 'AC',
                    'time': '1 ms'
                }
            ),
            # C (Clang 10.0.0)
            (
                'https://atcoder.jp/contests/abc170/submissions/14414384',
                {
                    'problem': 'A - Five Variables',
                    'user': 'siratai628 ',
                    'lang': 'C (Clang 10.0.0)',
                    'length': '139 Byte',
                    'result': 'AC',
                    'time': '10 ms'
                }
            ),
            # C++ (Clang 10.0.0)
            (
                'https://atcoder.jp/contests/abc170/submissions/14290048',
                {
                    'problem': 'A - Five Variables',
                    'user': 'ryo_m ',
                    'lang': 'C++ (Clang 10.0.0)',
                    'length': '135 Byte',
                    'result': 'AC',
                    'time': '8 ms'
                }
            ),
            # Java (OpenJDK 11.0.6)
            (
                'https://atcoder.jp/contests/abc170/submissions/14298695',
                {
                    'problem': 'A - Five Variables',
                    'user': 'skaw ',
                    'lang': 'Java (OpenJDK 11.0.6)',
                    'length': '221 Byte',
                    'result': 'AC',
                    'time': '108 ms'
                }
            ),
            # Python (3.8.2)
            (
                'https://atcoder.jp/contests/abc170/submissions/14435034',
                {
                    'problem': 'A - Five Variables',
                    'user': 'erniogi ',
                    'lang': 'Python (3.8.2)',
                    'length': '29 Byte',
                    'result': 'AC',
                    'time': '26 ms'
                }
            ),
            # Ruby (2.7.1)
            (
                'https://atcoder.jp/contests/abc170/submissions/14283850',
                {
                    'problem': 'A - Five Variables',
                    'user': 'n4o847 ',
                    'lang': 'Ruby (2.7.1)',
                    'length': '24 Byte',
                    'result': 'AC',
                    'time': '55 ms'
                }
            ),
            # C# (.NET Core 3.1.201)
            (
                'https://atcoder.jp/contests/abc170/submissions/14435215',
                {
                    'problem': 'A - Five Variables',
                    'user': 'Perilla ',
                    'lang': 'C# (.NET Core 3.1.201)',
                    'length': '125 Byte',
                    'result': 'AC',
                    'time': '95 ms'
                }
            ),
            # PyPy3 (7.3.0)
            (
                'https://atcoder.jp/contests/abc170/submissions/14368206',
                {
                    'problem': 'A - Five Variables',
                    'user': 'c_r_5 ',
                    'lang': 'PyPy3 (7.3.0)',
                    'length': '29 Byte',
                    'result': 'AC',
                    'time': '64 ms'
                }
            ),
            # Haskell (GHC 8.8.3)
            (
                'https://atcoder.jp/contests/abc170/submissions/14381674',
                {
                    'problem': 'A - Five Variables',
                    'user': 'Metarin ',
                    'lang': 'Haskell (GHC 8.8.3)',
                    'length': '43 Byte',
                    'result': 'AC',
                    'time': '8 ms'
                }
            ),
            # Rust (1.42.0)
            (
                'https://atcoder.jp/contests/abc170/submissions/14435774',
                {
                    'problem': 'A - Five Variables',
                    'user': 'atetubou ',
                    'lang': 'Rust (1.42.0)',
                    'length': '150 Byte',
                    'result': 'AC',
                    'time': '7 ms'
                }
            ),
        ]
        for url, ans in test_patterns:
            with self.subTest(url=url, ans=ans):
                self.assertEqual(get_submission_info(get_soup(url), url), ans)

    def test_get_contest_title(self):
        test_patterns = [
            ('https://atcoder.jp/contests/abc170/submissions/14351771',
             'AtCoder Beginner Contest 170'),
            ('https://atcoder.jp/contests/abc170/submissions/14351771?lang=ja',
                'AtCoder Beginner Contest 170'),
            ('https://atcoder.jp/contests/abc170/submissions/14351771?lang=en',
                'AtCoder Beginner Contest 170'),
            ('https://atcoder.jp/contests/tokiomarine2020/submissions/14219032',
                'Tokio Marine & Nichido Fire Insurance Programming Contest 2020'),
            ('https://atcoder.jp/contests/tokiomarine2020/submissions/14219032?lang=ja',
                '東京海上日動 プログラミングコンテスト2020'),
        ]
        for url, ans in test_patterns:
            with self.subTest(url=url, ans=ans):
                self.assertEqual(get_contest_title(get_soup(url), url), ans)

    def test_get_tweet_title(self):
        test_patterns = [
            ('https://atcoder.jp/contests/abc170/submissions/14465204',
             'Submission #14465204 - AtCoder Beginner Contest 170 https://atcoder.jp/contests/abc170/submissions/14465204?lang=en'),
            ('https://atcoder.jp/contests/abc170/submissions/14465204?lang=ja',
             '提出 #14465204 - AtCoder Beginner Contest 170 https://atcoder.jp/contests/abc170/submissions/14465204?lang=ja'),
            ('https://atcoder.jp/contests/abc170/submissions/14465204?lang=en',
             'Submission #14465204 - AtCoder Beginner Contest 170 https://atcoder.jp/contests/abc170/submissions/14465204?lang=en'),
        ]
        for url, ans in test_patterns:
            with self.subTest(url=url, ans=ans):
                self.assertEqual(get_tweet_title(get_soup(url), url), ans)

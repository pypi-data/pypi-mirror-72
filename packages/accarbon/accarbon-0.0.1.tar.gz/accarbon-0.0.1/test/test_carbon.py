# -*- coding: utf-8 -*-

from accarbon_command.carbon import get_lang_para
from unittest import TestCase


class TestCarbon(TestCase):
    def test_get_lang_para(self):
        test_patterns = [
            ('C (GCC 9.2.1)', 'text/x-csrc'),
            ('C (Clang 10.0.0)', 'text/x-csrc'),
            ('C++ (GCC 9.2.1)', 'text/x-c++src'),
            ('C++ (Clang 10.0.0)', 'text/x-c++src'),
            ('Java (OpenJDK 11.0.6)', 'text/x-java'),
            ('Python (3.8.2)', 'python'),
            ('Ruby (2.7.1)', 'ruby'),
            ('C# (.NET Core 3.1.201)', 'text/x-csharp'),
            ('PyPy3 (7.3.0)', 'python'),
            ('Haskell (GHC 8.8.3)', 'haskell'),
            ('Rust (1.42.0)', 'rust'),
            ('Brainfuck (bf 20041219)', 'auto'),
        ]
        for lang, ans in test_patterns:
            with self.subTest(lang=lang, ans=ans):
                self.assertEqual(get_lang_para(lang), ans)

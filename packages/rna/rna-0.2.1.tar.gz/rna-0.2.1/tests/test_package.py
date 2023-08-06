#!/usr/bin/env python

"""Tests for `rna` package."""

import unittest


class Test_rna(unittest.TestCase):
    """Tests for `rna` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_version_type(self):
        """Assure that version type is str."""
        import rna
        self.assertIsInstance(rna.__version__, str)

from unittest.case import TestCase

import os
from unittest.mock import patch, call

from python_scripts.filter_duplicated_unmapped import filter_duplicated_unmpped_read


class TestFilterDupUnmapped(TestCase):

    asset_dir = os.path.join(os.path.dirname(__file__), 'assets')

    def test_filter_duplicated_unmpped_read(self):
        input_file = os.path.join(self.asset_dir, 'test.bam')
        output_file = os.path.join(self.asset_dir, 'test_out.bam')
        with patch('sys.stderr.write') as patch_write:
            filter_duplicated_unmpped_read(input_file, output_file)
            assert patch_write.mock_calls[0] == call(
                'Read 17 reads from /Users/tcezard/PycharmProjects/Small_tools/tests/assets/test.bam\n'
            )
            assert patch_write.mock_calls[1] == call('Skipped 1 reads\n')

    def tearDown(self):
        output_file = os.path.join(self.asset_dir, 'test_out.bam')
        if os.path.exists(output_file):
            os.unlink(output_file)
            os.unlink(output_file + '.bai')


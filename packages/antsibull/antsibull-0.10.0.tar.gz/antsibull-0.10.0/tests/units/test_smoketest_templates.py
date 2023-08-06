import pytest

import pkgutil
from antsibull import dependency_files as df


def test_templates_compile(template_name):
    """Test that the jinja templates compile."""
    pieces_filename = tmp_path / 'pieces.in'
    with open(pieces_filename, 'w') as f:
        f.write(PIECES)
    assert df.parse_pieces_file(pieces_filename) == PARSED_PIECES

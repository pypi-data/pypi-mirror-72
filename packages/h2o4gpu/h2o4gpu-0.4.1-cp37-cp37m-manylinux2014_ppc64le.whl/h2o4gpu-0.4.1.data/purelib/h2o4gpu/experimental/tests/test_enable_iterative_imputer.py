"""Tests for making sure experimental imports work as expected."""

import textwrap

from h2o4gpu.utils.testing import assert_run_python_script


def test_imports_strategies():
    # Make sure different import strategies work or fail as expected.

    # Since Python caches the imported modules, we need to run a child process
    # for every test case. Else, the tests would not be independent
    # (manually removing the imports from the cache (sys.modules) is not
    # recommended and can lead to many complications).

    good_import = """
    from h2o4gpu.experimental import enable_iterative_imputer
    from h2o4gpu.impute import IterativeImputer
    """
    assert_run_python_script(textwrap.dedent(good_import))

    good_import_with_ensemble_first = """
    import h2o4gpu.ensemble
    from h2o4gpu.experimental import enable_iterative_imputer
    from h2o4gpu.impute import IterativeImputer
    """
    assert_run_python_script(textwrap.dedent(good_import_with_ensemble_first))

    bad_imports = """
    import pytest

    with pytest.raises(ImportError):
        from h2o4gpu.impute import IterativeImputer

    import h2o4gpu.experimental
    with pytest.raises(ImportError):
        from h2o4gpu.impute import IterativeImputer
    """
    assert_run_python_script(textwrap.dedent(bad_imports))

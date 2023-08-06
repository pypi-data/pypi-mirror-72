"""Enables histogram-based gradient boosting estimators.

The API and results of these estimators might change without any deprecation
cycle.

Importing this file dynamically sets the
:class:`h2o4gpu.ensemble.HistGradientBoostingClassifierSklearn` and
:class:`h2o4gpu.ensemble.HistGradientBoostingRegressorSklearn` as attributes of the
ensemble module::

    >>> # explicitly require this experimental feature
    >>> from h2o4gpu.experimental import enable_hist_gradient_boosting  # noqa
    >>> # now you can import normally from ensemble
    >>> from h2o4gpu.ensemble import HistGradientBoostingClassifierSklearn
    >>> from h2o4gpu.ensemble import HistGradientBoostingRegressorSklearn


The ``# noqa`` comment comment can be removed: it just tells linters like
flake8 to ignore the import, which appears as unused.
"""

from ..ensemble._hist_gradient_boosting.gradient_boosting import (
    HistGradientBoostingClassifierSklearn,
    HistGradientBoostingRegressorSklearn
)

from .. import ensemble

ensemble.HistGradientBoostingClassifierSklearn = HistGradientBoostingClassifierSklearn
ensemble.HistGradientBoostingRegressorSklearn = HistGradientBoostingRegressorSklearn
ensemble.__all__ += ['HistGradientBoostingClassifierSklearn',
                     'HistGradientBoostingRegressorSklearn']

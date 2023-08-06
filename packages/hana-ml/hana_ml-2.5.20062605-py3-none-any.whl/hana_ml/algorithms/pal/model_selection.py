"""
Model Selection
"""
from hana_ml.algorithms.pal.unified_classification import UnifiedClassification
#pylint: disable=too-many-arguments
#pylint: disable=useless-object-inheritance
#disable=old-style-class, super-on-old-class

class ParamSearchCV(object):
    """
    Exhaustive or random search over specified parameter values for an estimator.

    Parameters
    ----------
    estimator : estimator object
        This is assumed to implement the PAL estimator interface.
    param_grid : dict
        Dictionary with parameters names (string) as keys and lists of parameter settings \
        to try as values in which case the grids spanned by each dictionary in the list \
        are explored.\
        This enables searching over any sequence of parameter settings.
    train_control : dict
        Controlling parameters for model evaluation and parameter selection.
    scoring : str
        A string to evaluate the predictions.
    search_strategy : str
        ``grid`` or ``random``.
    """
    estimator = None
    def __init__(self,
                 estimator,
                 param_grid,
                 train_control,
                 scoring,
                 search_strategy):
        if isinstance(estimator, UnifiedClassification):
            func = None
            for key_ in estimator.func_dict:
                if estimator.func_dict[key_] == estimator.func:
                    func = key_
                    break
            estimator.__init__(func,
                               **dict(param_search_strategy=search_strategy,
                                      metric=scoring,
                                      param_values=param_grid,
                                      **train_control))
        else:
            estimator.add_attribute("param_search_strategy", search_strategy)
            estimator.add_attribute("search_strategy", search_strategy)
            estimator.add_attribute("resampling_method", "cv")
            #estimator.add_attribute("metric", scoring.upper())
            estimator.add_attribute("evaluation_metric", scoring.upper())
            for key, val in train_control.items():
                estimator.add_attribute(key, val)
            param_values = []
            for key, val in param_grid.items():
                if not isinstance(val, list):
                    val = [val]
                param_values.extend([(key, val)])
            estimator.add_attribute("param_values", param_values)
        self.estimator = estimator

    def set_timeout(self, timeout):
        """
        Specifies maximum running time for model evaluation or parameter selection, in seconds.
        No timeout when 0 is specified.
        """
        if isinstance(self.estimator, UnifiedClassification):
            self.estimator.update_cv_params('timeout', timeout, int)
        else:
            self.estimator.add_attribute("timeout", timeout)

    def set_seed(self, seed, seed_name=None):
        """
        Specifies the seed for random generation.
        Use system time when 0 is specified.
        """
        if isinstance(self.estimator, UnifiedClassification):
            self.estimator.update_cv_params('random_state', seed, int)
        else:
            if seed_name is not None:
                self.estimator.add_attribute(seed_name, seed)
            else:
                self.estimator.add_attribute("random_state", seed)

    def set_resampling_method(self, method):
        """
        Specifies the resampling method for model evaluation or parameter selection.
        - cv
        - stratified_cv
        - bootstrap
        - stratified_bootstrap

        stratified_cv and stratified_bootstrap can only apply to classification algorithms.
        """
        if isinstance(self.estimator, UnifiedClassification):
            self.estimator.update_cv_params('resampling_method', method, str)
        else:
            self.estimator.add_attribute("resampling_method", method)

    def set_scoring_metric(self, metric):
        """
        Specifies the evaluation metric for model evaluation or parameter selection.
        - accuracy
        - error_rate
        - f1_score
        - rmse
        - mae
        - auc
        - nll (negative log likelihood)
        """
        if isinstance(self.estimator, UnifiedClassification):
            self.estimator.update_cv_params('evaluation_metric', metric, str)
        else:
            self.estimator.add_attribute("metric", metric.upper())
            self.estimator.add_attribute("evaluation_metric", metric.upper())

    def fit(self, data, **kwargs):
        """
        Fit function.
        """
        self.estimator.fit(data, **kwargs)

    def predict(self, data, **kwargs):
        """
        Predict function.
        """
        return self.estimator.predict(data, **kwargs)

class GridSearchCV(ParamSearchCV):
    """
    Exhaustive search over specified parameter values for an estimator.

    Parameters
    ----------
    estimator : estimator object
        This is assumed to implement the PAL estimator interface.
    param_grid : dict
        Dictionary with parameters names (string) as keys and lists of parameter settings \
        to try as values in which case the grids spanned by each dictionary in the list \
        are explored.\
        This enables searching over any sequence of parameter settings.
    train_control : dict
        Controlling parameters for model evaluation and parameter selection.
    scoring : str
        A string to evaluate the predictions.
    """
    def __init__(self,
                 estimator,
                 param_grid,
                 train_control,
                 scoring):
        super(GridSearchCV, self).__init__(estimator,
                                           param_grid,
                                           train_control,
                                           scoring,
                                           "grid")

class RandomSearchCV(ParamSearchCV):
    """
    Random search over specified parameter values for an estimator.

    Parameters
    ----------
    estimator : estimator object
        This is assumed to implement the PAL estimator interface.
    param_grid : dict
        Dictionary with parameters names (string) as keys and lists of parameter settings \
        to try as values in which case the grids spanned by each dictionary in the list \
        are explored.\
        This enables searching over any sequence of parameter settings.
    train_control : dict
        Controlling parameters for model evaluation and parameter selection.
    scoring : str
        A string to evaluate the predictions.
    """
    def __init__(self,
                 estimator,
                 param_grid,
                 train_control,
                 scoring):
        super(RandomSearchCV, self).__init__(estimator,
                                             param_grid,
                                             train_control,
                                             scoring,
                                             "random")

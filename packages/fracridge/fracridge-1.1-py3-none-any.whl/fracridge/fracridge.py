"""

"""
import numpy as np
from numpy import interp
import warnings

from sklearn.base import BaseEstimator, MultiOutputMixin
from sklearn.utils.validation import (check_X_y, check_array, check_is_fitted,
                                      _check_sample_weight)

from sklearn.linear_model._base import _preprocess_data, _rescale_data

# Module-wide constants
BIG_BIAS = 10e3
SMALL_BIAS = 10e-3
BIAS_STEP = 0.2


__all__ = ["fracridge", "vec_len", "FracRidge"]


def fracridge(X, y, fracs=None, tol=1e-6, jit=True):
    """
    Approximates alpha parameters to match desired fractions of OLS length.

    Parameters
    ----------
    X : ndarray, shape (n, p)
        Design matrix for regression, with n number of
        observations and p number of model parameters.

    y : ndarray, shape (n, b)
        Data, with n number of observations and b number of targets.

    fracs : float or 1d array, optional
        The desired fractions of the parameter vector length, relative to
        OLS solution. If 1d array, the shape is (f,).
        Default: np.arange(.1, 1.1, .1)

    jit : bool, optional
        Whether to speed up computations by using a just-in-time compiled
        version of core computations. This may not work well with very large
        datasets. Default: True

    Returns
    -------
    coef : ndarray, shape (p, f, b)
        The full estimated parameters across units of measurement for every
        desired fraction.
    alphas : ndarray, shape (f, b)
        The alpha coefficients associated with each solution
    Examples
    --------
    Generate random data:
    >>> np.random.seed(0)
    >>> y = np.random.randn(100)
    >>> X = np.random.randn(100, 10)

    Calculate coefficients with naive OLS:
    >>> coef = np.linalg.inv(X.T @ X) @ X.T @ y
    >>> print(np.linalg.norm(coef))  # doctest: +NUMBER
    0.35

    Call fracridge function:
    >>> coef2, alpha = fracridge(X, y, 0.3)
    >>> print(np.linalg.norm(coef2))  # doctest: +NUMBER
    0.10
    >>> print(np.linalg.norm(coef2) / np.linalg.norm(coef))  # doctest: +NUMBER
    0.3

    Calculate coefficients with naive RR:
    >>> alphaI = alpha * np.eye(X.shape[1])
    >>> coef3 = np.linalg.inv(X.T @ X + alphaI) @ X.T @ y
    >>> print(np.linalg.norm(coef2 - coef3))  # doctest: +NUMBER
    0.0
    """
    # Per default, we'll try to use the jit-compiled SVD, which should be
    # more performant:
    use_scipy = False
    if jit:
        try:
            from ._linalg import svd
        except ImportError:
            warnings.warn("The `jit` key-word argument is set to `True` ",
                          "but numba could not be imported, or just-in time ",
                          "compilation failed. Falling back to ",
                          "`scipy.linalg.svd`")
            use_scipy = True

    # If that doesn't work, or you asked not to, we'll use scipy SVD:
    if not jit or use_scipy:
        from functools import partial
        from scipy.linalg import svd  # noqa
        svd = partial(svd, full_matrices=False)

    if fracs is None:
        fracs = np.arange(.1, 1.1, .1)

    if not hasattr(fracs, "__len__"):
        fracs = [fracs]
    fracs = np.array(fracs)

    nn, pp = X.shape
    if len(y.shape) == 1:
        y = y[:, np.newaxis]

    bb = y.shape[-1]
    ff = fracs.shape[0]

    uu, selt, v_t = svd(X)

    # This rotates the targets by the unitary matrix uu.T:
    ynew = uu.T @ y
    del uu

    # Solve OLS for the rotated problem and replace y:
    ols_coef = (ynew.T / selt).T
    del ynew

    # Set solutions for small eigenvalues to 0 for all targets:
    isbad = selt < tol
    if np.any(isbad):
        warnings.warn("Some eigenvalues are being treated as 0")

    ols_coef[isbad, ...] = 0

    # Limits on the grid of candidate alphas used for interpolation:
    val1 = BIG_BIAS * selt[0] ** 2
    val2 = SMALL_BIAS * selt[-1] ** 2

    # Generates the grid of candidate alphas used in interpolation:
    alphagrid = np.concatenate(
        [np.array([0]),
         10 ** np.arange(np.floor(np.log10(val2)),
                         np.ceil(np.log10(val1)), BIAS_STEP)])

    # The scaling factor applied to coefficients in the rotated space is
    # lambda**2 / (lambda**2 + alpha), where lambda are the singular values
    seltsq = selt**2
    sclg = seltsq / (seltsq + alphagrid[:, None])
    sclg_sq = sclg**2

    # Prellocate the solution:
    if nn >= pp:
        first_dim = pp
    else:
        first_dim = nn

    coef = np.empty((first_dim, ff, bb))
    alphas = np.empty((ff, bb))

    # The main loop is over targets:
    for ii in range(y.shape[-1]):
        # Applies the scaling factors per alpha
        newlen = np.sqrt(sclg_sq @ ols_coef[..., ii]**2).T
        # Normalize to the length of the unregularized solution,
        # because (alphagrid[0] == 0)
        newlen = (newlen / newlen[0])
        # Perform interpolation in a log transformed space (so it behaves
        # nicely), avoiding log of 0.
        temp = interp(fracs, newlen[::-1], np.log(1 + alphagrid)[::-1])
        # Undo the log transform from the previous step
        targetalphas = np.exp(temp) - 1
        # Allocate the alphas for this target:
        alphas[:, ii] = targetalphas
        # Calculate the new scaling factor, based on the interpolated alphas:
        sc = seltsq / (seltsq + targetalphas[np.newaxis].T)
        # Use the scaling factor to calculate coefficients in the rotated
        # space:
        coef[..., ii] = (sc * ols_coef[..., ii]).T

    # After iterating over all targets, we unrotate using the unitary v
    # matrix and reshape to conform to desired output:
    coef = np.reshape(v_t.T @ coef.reshape((first_dim, ff * bb)),
                      (pp, ff, bb))

    return coef.squeeze(), alphas


class FracRidge(BaseEstimator, MultiOutputMixin):
    """
    Fractional Ridge Regression estimator



    Parameters
    ----------
    fracs : float or sequence
        The desired fractions of the parameter vector length, relative to
        OLS solution. If 1d array, the shape is (f,).
        Default: np.arange(.1, 1.1, .1)


    Examples
    --------
    Generate random data:
    >>> np.random.seed(1)
    >>> y = np.random.randn(100)
    >>> X = np.random.randn(100, 10)

    Calculate coefficients with naive OLS:
    >>> coef = np.linalg.inv(X.T @ X) @ X.T @ y

    Initialize the estimator with a single fraction:
    >>> fr = FracRidge(fracs=0.3)

    Fit estimator:
    >>> fr.fit(X, y)
    FracRidge(fracs=0.3)

    Check results:
    >>> coef_ = fr.coef_
    >>> alpha_ = fr.alpha_
    >>> print(np.linalg.norm(coef_) / np.linalg.norm(coef)) # doctest: +NUMBER
    0.29
    """
    def _more_tags(self):
        return {'multioutput': True}

    def __init__(self, fracs=None, fit_intercept=False, normalize=False,
                 copy_X=True, tol=1e-6, jit=True):
        self.fracs = fracs
        self.fit_intercept = fit_intercept
        self.normalize = normalize
        self.copy_X = copy_X
        self.tol = tol
        self.jit = jit

    def fit(self, X, y, sample_weight=None):
        X, y = check_X_y(X, y, y_numeric=True, multi_output=True)

        if sample_weight is not None:
            sample_weight = _check_sample_weight(sample_weight, X,
                                                 dtype=X.dtype)

        X, y, X_offset, y_offset, X_scale = _preprocess_data(
            X, y, fit_intercept=self.fit_intercept, normalize=self.normalize,
            copy=self.copy_X, sample_weight=sample_weight,
            return_mean=True)

        if sample_weight is not None:
            # Sample weight can be implemented via a simple rescaling.
            X, y = _rescale_data(X, y, sample_weight)

        self.is_fitted_ = True
        coef, alpha = fracridge(X, y, fracs=self.fracs, tol=self.tol,
                                jit=self.jit)
        self.alpha_ = alpha
        self.coef_ = coef
        self._set_intercept(X_offset, y_offset, X_scale)
        return self

    def predict(self, X):
        X = check_array(X, accept_sparse=True)
        check_is_fitted(self, 'is_fitted_')
        pred = np.tensordot(X, self.coef_, axes=(1))
        if self.fit_intercept:
            pred = pred + self.intercept_
        return pred

    def _set_intercept(self, X_offset, y_offset, X_scale):
        """Set the intercept_
        """
        if self.fit_intercept:
            if len(self.coef_.shape) <= 2:
                self.coef_ = self.coef_ / X_scale[:, np.newaxis]
            else:
                self.coef_ = self.coef_ / X_scale[:, np.newaxis, np.newaxis]
            self.intercept_ = y_offset - np.tensordot(X_offset,
                                                      self.coef_, axes=(1))
        else:
            self.intercept_ = 0.


def vec_len(vec, axis=0):
    return np.sqrt((vec * vec).sum(axis=axis))


def optimize_for_frac(X, fracs):
    """
    Empirically find the alpha that gives frac reduction in vector length of
    the solution

    """
    u, s, v = svd(X)

    val1 = 10e3 * s[0] ** 2  # Huge bias
    val2 = 10e-3 * s[-1] ** 2  # Tiny bias

    alphas = np.concatenate(
        [np.array([0]), 10 ** np.arange(np.floor(np.log10(val2)),
                                        np.ceil(np.log10(val1)), 0.1)])

    results = np.zeros(alphas.shape[0])
    for ii, alpha in enumerate(alphas):
        results[ii] = frac_reduction(X, alpha, s=s)

    return interp1d(results, alphas, bounds_error=False, fill_value="extrapolate")(np.asarray(fracs))


def frac_reduction(X, alpha, s=None):
    """
    Calculates the expected fraction reduction in the length of the
    coefficient vector $\beta$ from OLS to ridge, given a design matrix X and
    a regularization metaparameter alpha.
    """
    if s is None:
        u, s, v = svd(X)
    new = s / (s ** 2 + alpha)
    olslen = np.sqrt(np.sum((1 / s) ** 2))
    rrlen = np.sqrt(np.sum(new ** 2))
    return rrlen / olslen


def frac_reduction_flat(X, alpha, s=None):
    """
    This is the version that assumes a flat eigenvalue spectrum
    """
    if s is None:
        u, s, v = svd(X)
    return np.mean(s ** 2 / (s ** 2 + alpha))


def reg_alpha_flat(X, gamma, s=None):
    """
    This is the version that assumes a flat eigenvalue spectrum
    """
    if s is None:
        u, s, v = svd(X)
    return (s ** 2) * (1 / gamma - 1)

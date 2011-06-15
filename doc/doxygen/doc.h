/*! \mainpage
 *
 * \section summary Summary
 *
 * The goal of this project is to extend GNU Radio with proper spectral estimation routines, i.e. algorithms that have been mathematically analyzed. The toolbox includes the following algorithms:
 *
 * - Welch's method, the most commonly used non-parametric algorithm.
 * - Burg's method, a popular parametric algorithm. The coefficients can also be directly accessed e.g. to parametrise an adaptive filter.
 * - Thompson's multitaper method (MTM), which uses multiple Discrete Prolate Spheroidal Sequences as data tapers to reduce the variance of the spectrum estimate. This was added as part of a Bachelor thesis which can be downloaded here. 
 * \image html specest_welch.png
 */

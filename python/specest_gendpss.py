#!/usr/bin/env python

import math
from gnuradio import gr

## generates the first K slepian sequences 
# @param N: Length of the FFT
# @param NW: Time Bandwidth Product usually is of value 2, 2.5, 3.0, 3.5, or 4
# @param K: Numbers of Tapers to use. K should be smaller than 2*NW
# @param EPS: sets the accuracy with which the eigenvalue of the T-Matrix are computed. Default value is 1E-6.
#		If EPS is set to \f$ \epsilon \f$ it follows for the estimated eigenvalue \f$ \lambda_e \in [ \lambda - \epsilon, \lambda + \epsilon ]\f$ with \f$ \lambda \f$ being the true eigenvalue \n
# @param DELTA: sets the accuracy of the DPSS computation. Default value is 1E-6
#		If DELTA is set to \f$ \Delta \f$ the computation of the eigenvector stops as soon as the first component of the eigenvector changes less than \f$ \Delta \f$ after an iteration.
class gendpss():
    # Generates DPSS utilizing the algorithm given in 
    # "A Simple Algorithm for Generating Disgrete Prolate Spheroidal Sequences" D.M. Gruenenbacher, D.R. Hummels IEEE Vol 42 11. November 1994 \n
    def __init__(self, N = 512 , NW = 3 , K = 5, weighting = 'unity', EPS=1E-6, DELTA=1E-6):
        self.N = N
        self.NW = NW
        self.K = K
        self.weighting = weighting
        self.EPS = EPS
        self.DELTA = DELTA
        self.W = float(self.NW)/N
        # cosfac and nfac save some computation time because they do not change during the execution of the following while-loop
        cosfac = math.cos( 2 * math.pi * self.W )
        nfac = (N-1)/2.
        # generates the t-matrix
        self.diag = [1.0] * N
        self.subdiag = [0.0] * (N-1)
        self.diag[0] = (nfac**2)*cosfac
        i = 1
        while i < N:
            self.diag[i] = ( (nfac-i)**2 )*cosfac
            self.subdiag[i-1] = (1./2.)*i*(N-i)
            i = i + 1
        # space to save the eigenvalues and eigenvectors
        self.lambdas = []
        eigenvector = [1.1]*N
        self.dpssarray = []
        i = 0
        while i < K:
            self.lambdas.append(self.func_get_eigenvalue( k=N-(i+1)))
            self.dpssarray.append(eigenvector[:])
            while True:
                oldeigenvector = self.dpssarray[i][0]
                self.dpssarray[i] = self.func_eigval2eigvec(eigenvalue = self.lambdas[i],d=self.dpssarray[i])
                if DELTA > math.fabs( math.fabs(oldeigenvector) - math.fabs(self.dpssarray[i][0]) ):
                    break
            self.lambdas[i] = self.func_get_SINC_eigval(self.dpssarray[i])
            i = i + 1

    ## Returns a sequence which contains all the sign changes of the characteristic polynoms of the T-Matrix at x
    # the number of sign changes is equal to the number of eigenvalues which are smaller than x
    # @param x: the value for which the characteristic polynoms are computed
    # @return: returns a sequence which contains all the sign changes of the characteristic polynoms
    def func_charpol(self,x):
        charpol = [0.0]*(self.N+1) # a NxN-matrix has N+1 "sub"characteristic polynoms
        charpol[0] = 1
        charpol[1] = self.diag[0] - x
        i = 2
        # See Golub and Van Loan, "Matrix Computations" 1989 2nd ed. page 437 for details about recursive relationship
        while i <= self.N:
            #we can calculate our subcharacteristic polynoms recursively
            charpol[i] = ( self.diag[i-1] - x )*charpol[i-1] - ( (self.subdiag[i-2])**2 )*charpol[i-2]
            # this is necessary because if N is large enough charpol[i] becomes extremely large and at one point python can no longer cope with these large numbers.
            # changing of charpol[i] is possible since we are only interested in the sign of the results and not the absolute value of them
            if math.fabs(charpol[i]) > 1E10:
                charpol[i] /= math.fabs(charpol[i-1])
                charpol[i-1] /= math.fabs(charpol[i-1])
            charpol[i-2] /= math.fabs(charpol[i-2])
            i = i + 1
        return charpol


    ## Gives back the number of sign changes in a sequence
    # @param seq: 
    # @return: the number of sign-changes in seq
    def func_signchanges(self,seq):
        count = 0
        i = 1
        while i < len(seq):
            p = seq[i-1]
            pp = seq[i]
            if p*pp <= 0:
                count = count + 1
            i = i + 1
        return count

    ## Calculates the kth eigenvalue of the T-Matrix
    # @return: the kth eigenvalue
    def func_get_eigenvalue(self,k):	
        # the interval in which the eigenvalues can be found is limited by the Gershgorin circle theorem. See Golub and Van Loan, "Matrix Computations" 1989 2nd ed. p341
        maxrange = 0.125*( (self.N-1)*(self.N+2) + self.N*(self.N+1) ) + 0.25
        lmax = maxrange
        lmin = -maxrange
        seq = [0.0]*(self.N+1)
        while math.fabs(lmax - lmin) > self.EPS: # EPS sets the accuracy with which the eigenvalues are computed
            lambda_k = (lmax + lmin)/2
            seq=self.func_charpol(x=lambda_k)
            if self.func_signchanges(seq) >= k+1:
                lmax = lambda_k
            else:
                lmin = lambda_k
        return lambda_k

    ## Calculates the eigenvector to a corresponding eigenvalue
    # this is done by using inverse iteration (see F. S. Acton "Numerical Methods that work" 2nd ed 1990 p356)
    # This function is basically an implementation of the Thomas-Algorithm (http://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm) to solve the System of linear Equations
    # @param eigenvalue: the eigenvalue whose eigenvector is to be found
    # @param d: the estimate of the eigenvector used in the inverse iteration method
    def func_eigval2eigvec(self,eigenvalue,d):
        a = [0.0] * (self.N-1)
        b = [0.0] * self.N
        c = [0.0] * (self.N-1)
        k = 0
        j = 0
        #the matrix needs to be reseted after each iteration
        #it isnt really necessary to reset a because it doesnt change at all
        #b on the other hand needs a reset after change of the eigenvalue but not after each iteration
        #this leaves room for optimazition
        #setting up the Matrix (T - eigenvalue*I)
        while j < self.N-1:
            a[j] = self.subdiag[j]
            b[j] = self.diag[j] - eigenvalue
            c[j] = self.subdiag[j]
            j = j + 1
        b[j] = self.diag[j] - eigenvalue # a and c are shorter than b so b[N-1] must be assigned extra
        j = 0

        c[0] = c[0]/b[0]
        d[0] = d[0]/b[0]
        j = 1
        while j < self.N-1:
            id = 1/(b[j] - c[j-1]*a[j-1] ) #saves a little computation time
            c[j] = c[j] * id
            d[j] = ( d[j] - d[j-1]*a[j-1] ) * id
            j = j  + 1
        d[j] = ( d[j] - d[j-1]*a[j-1] ) / (b[j] - c[j-1]*a[j-1] )
        j = j - 1
        while j >= 0:
            d[j] = d[j] - c[j]*d[j+1]
            j = j - 1
        #normalize d
        d = self.func_normalizevector(d)
        return d

    ## Normalizes a vector
    # @param vector: the vector to be normalized
    # @return: the normalized vector
    def func_normalizevector(self,vector):
        j = 0
        sum = 0
        while j < len(vector):
            sum = sum + vector[j]**2
            j = j + 1
        sum = sum**0.5
        j = 0
        while j < len(vector):
            vector[j] = vector[j]/sum
            j = j + 1
        return vector

    ## Returns the eigenvalue of the sinc-matrix for a given eigenvector
    # @param eigenvector: the eigenvector whose eigenvalue is to be calculated
    # @return: the eigenvalue belonging to the given eigenvector
    def func_get_SINC_eigval(self,eigenvector):
        # get the index of the biggest element in our eigenvector. This is used because later we devide through a vector element and some dpss-values are close to zero, which could be critical.
    # speed can propably increased if you search for the biggest element and its index at the same time.
        k = eigenvector.index(max(eigenvector))
    # the eigenvalues lambda is calculated  by: A * v = lambda * v where A is the Sinc-Matrix. We don't need to do the full matrixmultiplication. One line suffices.
        linesinc = [0.0] * self.N
    # this code generates the kth line of the Sinc Matrix and multiplies it with the eigenvector
    # extra care must be taken since sin(x)/x can't be calculated by python for x = 0
        sum = 0
        i = 0
        while i < k:
            linesinc[i] = (math.sin(2*math.pi*self.W*(i-k)))/(math.pi*(i-k))
            sum += linesinc[i]*eigenvector[i]
            i = i + 1
        # this is the critical element since python can't compute sin(0)/0
        linesinc[k] = (2*self.W)
        sum += linesinc[0+k]*eigenvector[0+k]
        i = k + 1	
        while i < self.N:
            linesinc[i] = (math.sin(2*math.pi*self.W*(i-k)))/(math.pi*(i-k))
            sum += linesinc[i]*eigenvector[i]
            i = i + 1
        eigenvalue = sum/eigenvector[k]
        return eigenvalue


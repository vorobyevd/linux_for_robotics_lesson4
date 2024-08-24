#!/bin/python3

# Dependencies

import scipy.signal
import collections

#*********************************** Class lowpass filter **************************************

class LowpassFilter:
    """
        Class implements 2-nd order lowpass IIR filter 
    """
    def __init__(self,f_pass: float,f_sampling: float) -> None:
        """
        Initialisation of 2-nd order IIR filter
        :param f_pass: passsing frequency
        :type f_pass: float
        :param f_sampling: sampling frequency
        :type f_sampling: float
        """
        self.b_coeffs, self.a_coeffs = scipy.signal.iirfilter(2, Wn=f_pass, fs=f_sampling, btype="low", ftype="butter")
        self.x_fifo = collections.deque([0,0,0],3) # shift register for input values 
        self.y_fifo = collections.deque([0,0,0],3) # shift register for output values 
            
    def calculate_out(self, x_in: float) -> float:
        """
        Function calculates output value of IIR filter 
        :param x_in: input value
        :type x_in: float
        :return: filtered value
        :rtype: float
        """
        # Get input value
        self.x_fifo[0] = x_in

        # Difference equation of IIR filter obtained from transfer function Numerator/Denominator
        self.y_out =  self.x_fifo[0] * self.b_coeffs[0] + self.x_fifo[1] * self.b_coeffs[1] + self.x_fifo[2] * self.b_coeffs[2] \
                                                        - self.y_fifo[1] * self.a_coeffs[1] - self.y_fifo[2] * self.a_coeffs[2]
        self.y_fifo[0] = self.y_out
        
        # Shift buffers
        self.x_fifo.rotate()
        self.y_fifo.rotate()
        
        return self.y_out

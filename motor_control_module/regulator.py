#!/bin/python3

"""
    File regulator.py  contains regulators of different types

"""
 
 # ****************************** PI-regulator class ********************************

class PI_Regulator(object):
    """
    Class implements PI-regulator functionality

    """
    def __init__(   self,
                    Kp:float,
                    Ki:float ,
                    min_output:float, 
                    max_output:float
                ) -> None:
        """
        Initialisation of regulator

        :param Kp: proportional coefficient
        :type Kp: float
        :param Ki: integral coefficient
        :type Ki: float
        :param min_output: minimal output action
        :type min_output: float
        :param max_output: maximal output action
        :type max_output: float
        """
        self.Kp = Kp
        self.Ki = Ki
        self.min_output = min_output 
        self.max_output = max_output
        self.act_value  = 0
        self.integrator = 0
        self.output = 0
        self.output_limitation = True


    def enable_output_limitation(self) -> None:
        """ Method for enabling regulator output limitation"""

        self.enable_output_limitation = True


    def disable_output_limitation(self) -> None:
        """ Method for disabling regulator output limitation"""

        self.enable_output_limitation = False


    def calculate(self, setpoint:float, act_value:float) -> float:
        """
        Method for calculating of regulator action
        :param setpoint: setpoint value
        :type setpoint: float
        :param act_value: actual value from feedback
        :type act_value: float
        :return: control action
        :rtype: float

        """
        self.setpoint = setpoint
        self.act_value = act_value
        self.error = self.setpoint - self.act_value
        self.integrator += self.error
        self.output = self.Kp * self.error + self.integrator * self.Ki
      
        if ( self.output_limitation == True ):
            self.output = PI_Regulator.bound_value(self.output,self.min_output,self.max_output)
        
        return self.output
    
    @staticmethod
    def bound_value(input_value: float, min_value: float, max_value: float) ->float:
        """
        Function for limitation of numeric value
        :param input: input value
        :type input: float
        :param min_value: output value
        :type min_value: float
        :param max_value: maximum output value
        :type max_value: float
        :return: bounded output value
        :rtype: float
        """
        bounded_output = 0.0
        if ( input_value > max_value ):
            bounded_output = max_value
        elif ( input_value < min_value ):
            bounded_output = min_value
        else: bounded_output = input_value


        return bounded_output

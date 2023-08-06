class Calculator:
    """ Takes two arguments as an input, then returns the result of required computation.
    """    
    @staticmethod
    def gcd(num_1, num_2):
        """ Computes the GCD of two numbers
        Args(int) : two integers
        Returns(int) : Greatest Common Divisor of two numbers
        """
        num_1, num_2 = int(num_1), int(num_2)
        while num_2 != 0:
            num_1, num_2 = num_2, num_1%num_2
        return num_1
    
    @classmethod
    def lcm(cls, num_1, num_2):
        """ Computes the LCM of two numbers
        Args(int) : two integers
        Returns(int) : Lowest Common Multiple of two numbers
        """
        num_1, num_2 = int(num_1), int(num_2)
        gcd_value = cls.gcd(num_1, num_2)
        return (num_1*num_2)/gcd_value
    
    @classmethod
    def reduce_fraction(cls, numerator, denominator):
        """ Reduces the fraction
        Args(int) : two integers. 
                    First --> numerator of a fraction
                    Second --> denominator of a fraction
        Returns : Reduced numerator and denominator in tuple (reduced_numerator, reduced_denominator)
        """
        numerator, denominator = int(numerator), int(denominator)
        gcd_value = cls.gcd(numerator, denominator)

        if (numerator==0) and (denominator==0):
            return "Division by 0 error"
        else:
            return (numerator//gcd_value, denominator//gcd_value)

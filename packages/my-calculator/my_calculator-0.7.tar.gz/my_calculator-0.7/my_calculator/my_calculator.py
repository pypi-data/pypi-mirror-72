class Calculator:

    """ Takes multiple arguments as an input, then returns the result of required computation.
    """

    @staticmethod
    def gcd_finder(num_1, num_2):
        """ Computes the GCD of two numbers
        Args(int) : two integers
        Returns(int) : Greatest Common Divisor of two numbers
        """

        (num_1, num_2) = (int(num_1), int(num_2))
        while num_2 != 0:
            (num_1, num_2) = (num_2, num_1 % num_2)
        return num_1

    @classmethod
    def gcd(cls, *args):
        """ Computes the GCD of list of numbers
        Args(int) : integers list
        Returns(int) : Greatest Common Divisor of list of numbers
        """

        if len(args) == 1:
            return args[0]
        args = [int(i) for i in args]  # Conversion to integer
        gcd_value = cls.gcd_finder(args[0], args[1])
        for index in range(2, len(args)):
            gcd_value = cls.gcd_finder(gcd_value, args[index])
        return gcd_value

    @classmethod
    def lcm_finder(cls, num_1, num_2):
        """ Computes the LCM of two numbers
        Args(int) : two integers
        Returns(int) : Lowest Common Multiple of two numbers
        """

        gcd_value = cls.gcd(num_1, num_2)
        return int(num_1 * num_2 / gcd_value)

    @classmethod
    def lcm(cls, *args):
        """ Computes the LCM of list of numbers
        Args(int) : integers list
        Returns(int) : Greatest Common Divisor of list of numbers
        """

        if len(args) == 1:
            return args[0]
        args = [int(i) for i in args]  # Conversion to integer
        lcm_value = cls.lcm_finder(args[0], args[1])
        for index in range(2, len(args)):
            lcm_value = cls.lcm_finder(lcm_value, args[index])
        return int(lcm_value)

    @classmethod
    def reduce_fraction(cls, numerator, denominator):
        """ Reduces the fraction
        Args(int) : two integers. 
                    First --> numerator of a fraction
                    Second --> denominator of a fraction
        Returns : Reduced numerator and denominator in tuple (reduced_numerator, reduced_denominator)
        """

        (numerator, denominator) = (int(numerator), int(denominator))
        gcd_value = cls.gcd(numerator, denominator)

        if numerator == 0 and denominator == 0:
            return 'Division by 0 error'
        else:
            return (numerator // gcd_value, denominator // gcd_value)

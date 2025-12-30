from math import exp

def future_discrete_value(present_value, interest_rate, time):
    """
    Calculate the future value of a present amount with discrete compounding.

    :param present_value: The present amount of money.
    :param interest_rate: The annual interest rate (as a decimal).
    :param periods: The number of compounding periods.
    :return: The future value after the specified periods.
    """
    future_value = present_value * (1 + interest_rate) ** time
    return future_value

def future_continuous_value(present_value, interest_rate, time):

    """
    :param present_value: the present amount of money
    :param interest_rate: annual interest rate (as a decimal)
    :param time: time in years
    :return: future value with continuous compounding
    """
    future_value = present_value*exp(interest_rate*time)
    return future_value



if __name__ == '__main__':
    pv = 1000  # present value
    r = 0.05   # interest rate
    t = 10     # time in years

    fv_discrete = future_discrete_value(pv, r, t)
    fv_continuous = future_continuous_value(pv, r, t)

    print(f"Future Value with Discrete Compounding: ${fv_discrete:.2f}")
    print(f"Future Value with Continuous Compounding: ${fv_continuous:.2f}")
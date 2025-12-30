from math import exp

class ZeroCouponBond:
    def __init__(self, principal, maturity, interest_rate):
        self.principal = principal
        self.maturity = maturity
        self.interest_rate = interest_rate

    def present_value(self, period):

        value = self.principal / (1 + self.interest_rate) ** period
        return value


    def present_value_continuous(self, period):
        value = self.principal * exp(-self.interest_rate * period)

        return value


if __name__ == '__main__':
    bond = ZeroCouponBond(1000, 5, 0.05)
    pv = bond.present_value(5)
    print(f"Present Value of the Zero-Coupon Bond: {pv:.2f}")
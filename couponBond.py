from math import exp

class CouponBond:
    def __init__(self, principal, maturity, interest_rate, coupon_rate):
        self.principal = principal
        self.maturity = maturity
        self.interest_rate = interest_rate / 100
        self.coupon_rate = coupon_rate / 100

    def present_value(self, period):
        coupon_payment = self.principal * self.coupon_rate
        pv_coupons = sum(coupon_payment / (1 + self.interest_rate) ** t for t in range(1, period + 1))
        pv_principal = self.principal / (1 + self.interest_rate) ** period
        value = pv_coupons + pv_principal
        return value

    def present_value_continuous(self, period):
        coupon_payment = self.principal * self.coupon_rate
        pv_coupons = sum(coupon_payment * exp(-self.interest_rate * t) for t in range(1, period + 1))
        pv_principal = self.principal * exp(-self.interest_rate * period)
        value = pv_coupons + pv_principal
        return value


if __name__ == '__main__':
    bond = CouponBond(1000, 5, 5, 6)
    pv = bond.present_value(5)
    print(f"Present Value of the Coupon Bond: {pv:.2f}")
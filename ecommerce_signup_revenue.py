
"""
We will now model the DGP (Data Generation Process) of an eCommerce ad flow starting with sign-ups.

On any day, we get many ad impressions, which can be modeled as Poisson random variables (RV). You are told that λ is normally distributed with a mean of 100k visitors and standard deviation 2000.

During the signup journey, the customer sees an ad, decides whether or not to click, and then whether or not to signup. Thus both clicks and signups are binary, modeled using binomial RVs. What about probability p of success? Our current low-cost option gives us a click-through rate of 1% and a sign-up rate of 20%. A higher cost option could increase the clickthrough and signup rate by up to 20%, but we are unsure of the level of improvement, so we model it as a uniform RV.
"""


import matplotlib.pyplot as plt
import numpy as np


ct_rate = {"low": 0.01, "high": np.random.uniform(low=0.01, high=1.2*0.01)}
su_rate = {"low": 0.2, "high": np.random.uniform(low=0.2, high=1.2*0.2)}

def get_signups(cost, ct_rate, su_rate, sims):
    lam = np.random.normal(loc=100000, scale=2000, size=sims)
    # Simulate impressions(poisson), clicks (binomial) and signups(binomial)
    impressions = np.random.poisson(lam)
    clicks = np.random.binomial(impressions, ct_rate[cost])
    signups = np.random.binomial(clicks, su_rate[cost])
    return signups

print("Simulated Signups = {}".format(get_signups("high", ct_rate, su_rate, 1)))


def get_revenue(signups):
    rev = []
    np.random.seed(123)
    for s in signups:
        # Model purchases as binomial, purcase_values as exponential
        purchases = np.random.binomial(s, p=0.1)
        purchase_values = np.random.exponential(10000, size=purchases)

        # Append to revenue the sum of all purchase values.
        rev.append(np.sum(purchase_values))
    return rev

print("Simulated Revenue = ${}".format(get_revenue(get_signups("low", ct_rate, su_rate, 1))[0]))


# Probability of losing money


# Initialize cost_diff
sims, cost_diff = 10000, 3000

# Get revenue when the cost if 'low' and when the cost is 'high'
rev_low = get_revenue(get_signups('low', ct_rate, su_rate, sims))
rev_high = get_revenue(get_signups('high', ct_rate, su_rate, sims))

# calculate fraction of times rev_high - rev_low is less than cost_diff
frac = np.sum([1 for a, b in zip(rev_high, rev_low) if a-b < cost_diff])/len(rev_low)
print("Probability of losing money = {}".format(frac))



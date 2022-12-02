# References:
# https://www.calculatorsoup.com/calculators/math/gcf.php
# https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-euclidean-algorithm

from datetime import datetime
from math import sqrt


def get_gcf_and_runtime(selection: str, nums: list):
    start = datetime.now()
    gcf = algos[selection](nums)
    end = datetime.now()

    print(f"GCF: {gcf}")

    td = (end - start).total_seconds() * 10**3
    print(f"Runtime of {selection} Algorithm: {td:.03f}ms")


def euclidean(nums: list) -> int:

    if len(nums) > 2:
        # Replace the first two nums in the list with their GCF
        a = euclidean(nums[0:2])
        nums = [a]+nums[2:]
        return euclidean(nums)

    a = nums[0]
    b = nums[1]
    # print(f"A: {a}\nB: {b}")

    # If A = 0 then GCD(A,B)=B, since the GCD(0,B)=B, and we can stop.
    if a == 0:
        return b
    # If B = 0 then GCD(A,B)=A, since the GCD(A,0)=A, and we can stop.
    elif b == 0:
        return a

    # q = round(a/b)  # quotient
    r = a % b       # remainder

    # Write A in quotient remainder form (A = B⋅Q + R)
    # print(f"{a} = {b} * {q} + {r}\n")
    # Find GCD(B,R) using the Euclidean Algorithm since GCD(A,B) = GCD(B,R)
    return euclidean([b, r])  # def euclidean(nums):


def factoring(nums: list) -> int:

    def factorization(n: int) -> list:
        """Get all the factors of an integer"""
        s = sqrt(n).__floor__()
        factors = []
        for i in range(1, s+1):
            q = n/i  # quotient
            if q.is_integer():
                factors += [int(q), i]
        return set(factors)

    # Get sets of the factors of each number and add them to a list
    factors_sets = []
    for num in nums:
        factors_sets.append(factorization(num))

    # Get the common factors of all the numbers
    common_factors = set.intersection(*factors_sets)
    return max(common_factors)


algos = {
    "Euclidean": euclidean,
    "Factoring": factoring,
}


if __name__ == "__main__":
    list_one = [18, 27]
    list_two = [20, 50, 120]
    list_three = [182664, 154875, 137688]

    print("----")
    get_gcf_and_runtime("Euclidean", list_one)
    get_gcf_and_runtime("Factoring", list_one)
    print("----")
    get_gcf_and_runtime("Euclidean", list_two)
    get_gcf_and_runtime("Factoring", list_two)
    print("----")
    get_gcf_and_runtime("Euclidean", list_three)
    get_gcf_and_runtime("Factoring", list_three)

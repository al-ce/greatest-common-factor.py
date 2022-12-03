# References:
# https://www.calculatorsoup.com/calculators/math/gcf.php
# https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-euclidean-algorithm

from datetime import datetime
from math import sqrt
from functools import reduce


class Node:
    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None


class PrimeFactorTree:
    """Generate a binary tree of all the prime factor pairs of a number."""

    def __init__(self, value: int):
        # Initialize an empty list if this is the first call.
        self.primes = []
        self.root = self.prime_factorization(value)

    def prime_factorization(self, n: int):
        """Prime Factor Tree generator."""

        node = Node(n)

        if self.is_prime(n):
            self.primes.append(n)
            return node

        s = sqrt(n).__floor__()  # call .__floor__ to round down

        for i in range(2, s + 1):
            if node.value % i == 0:
                # print(f"n: {n} i: {i} n/i: {int(n/i)}")
                node.left == self.prime_factorization(i)
                node.right == self.prime_factorization(int(n/i))
                break

        return node

    def is_prime(self, n):
        """Return True if n is prime, else return False."""
        for i in range(2, int(n/2)):
            if (n % i) == 0:
                return False
        return True


def get_gcf_and_runtime(selection: str, nums: list):
    start = datetime.now()
    gcf = algos[selection](nums)
    end = datetime.now()

    print(f"GCF: {gcf}")

    td = (end - start).total_seconds() * 10**3
    print(f"Runtime of {selection} Algorithm: {td:.03f}ms")


def gcf_by_euclidean(nums: list) -> int:

    if len(nums) > 2:
        # Replace the first two nums in the list with their GCF
        a = gcf_by_euclidean(nums[0:2])
        nums = [a]+nums[2:]
        return gcf_by_euclidean(nums)

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
    return gcf_by_euclidean([b, r])  # def euclidean(nums):


def gcf_by_factoring(nums: list) -> int:

    # Get sets of the factors of each number and add them to a list
    factors_sets = []
    for num in nums:
        factors_sets.append(set(factorization(num)))

    # Get the common factors of all the numbers
    common_factors = set.intersection(*factors_sets)
    return max(common_factors)


def factorization(n: int) -> list:
    """Get all the factors of an integer"""
    s = sqrt(n).__floor__()  # call .__floor__ to round down
    factors = []
    for i in range(2, s+1):
        q = n/i  # quotient
        if q.is_integer():
            factors += [int(q), i]
    return factors


def gcf_by_prime_factorization(nums: list) -> int:
    prime_factors_lists = []
    for num in nums:
        primes = PrimeFactorTree(num).primes
        prime_factors_lists.append(primes)

    common_factors = set([p for primes in prime_factors_lists for p in primes])

    occurrences = []
    for p in common_factors:
        min_p = float('inf')
        for primes in prime_factors_lists:
            # Count the occurrences of p for this list of prime factors
            p_count = primes.count(p)
            if p_count < min_p:
                min_p = p_count
        # Add the highest number of occurrences of each prime factor that is
        # common to each number to occurrences list
        occurrences.extend([p for i in range(min_p)])

    gcf = reduce(lambda x, y: x*y, occurrences)
    return gcf


algos = {
    "Euclidean": gcf_by_euclidean,
    "Factoring": gcf_by_factoring,
    "Prime Factorization": gcf_by_prime_factorization,
}

if __name__ == "__main__":
    list_one = [18, 27]
    list_two = [20, 50, 120]
    list_three = [182664, 154875, 137688]

    print("----")
    get_gcf_and_runtime("Euclidean", list_one)
    get_gcf_and_runtime("Factoring", list_one)
    get_gcf_and_runtime("Prime Factorization", list_one)
    print("----")
    get_gcf_and_runtime("Euclidean", list_two)
    get_gcf_and_runtime("Factoring", list_two)
    get_gcf_and_runtime("Prime Factorization", list_three)
    print("----")
    get_gcf_and_runtime("Euclidean", list_three)
    get_gcf_and_runtime("Factoring", list_three)
    get_gcf_and_runtime("Prime Factorization", list_three)

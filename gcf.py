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

    def is_prime(self, n):
        """Return True if n is prime, else return False."""
        for i in range(2, int(n/2)):
            if (n % i) == 0:
                return False
        return True

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


class GCFCalculator:
    def __init__(self, nums: list):
        self.algos = {
            "Euclidean": self.gcf_by_euclidean,
            "Factoring": self.gcf_by_factoring,
            "Prime Factorization": self.gcf_by_prime_factorization,
        }
        self.results = self.get_gcf_and_algo_runtimes(nums)

    def bug_check(self, gcf_values: dict):
        """Raise an error if the algorithms return differing values."""
        gcfs = {gcf for gcf in gcf_values.values()}
        length = len(gcfs)

        if length == 1:
            return None

        msg = "Algorithms returned differing values.\n"

        for algo_name, gcf in gcf_values.items():
            msg += f"{algo_name:<20} algorithm returned {gcf}\n"
        raise Exception(msg)

    def convert_nums_to_str(self, nums):
        """Convert a list of numbers to a csv row."""
        nums_str = "Numbers:"
        for num in nums:
            nums_str += f" {num}"
        return nums_str

    def factorization(self, n: int) -> list:
        """Get all the factors of an integer"""
        s = sqrt(n).__floor__()  # call .__floor__ to round down
        factors = []
        for i in range(2, s+1):
            q = n/i  # quotient
            if q.is_integer():
                factors += [int(q), i]
        return factors

    def gcf_by_euclidean(self, nums: list) -> int:
        """Get the GCF of a list of nums with the Euclidean Algorithm."""

        if len(nums) > 2:
            # Replace the first two nums in the list with their GCF
            a = self.gcf_by_euclidean(nums[0:2])
            nums = [a]+nums[2:]
            return self.gcf_by_euclidean(nums)

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
        return self.gcf_by_euclidean([b, r])  # def euclidean(nums):

    def gcf_by_factoring(self, nums: list) -> int:

        # Get sets of the factors of each number and add them to a list
        factors_sets = []
        for num in nums:
            factors_sets.append(set(self.factorization(num)))

        # Get the common factors of all the numbers
        common_factors = set.intersection(*factors_sets)

        # If relatively prime, return 1, else gcf
        gcf = max(common_factors) if common_factors else 1

        return gcf

    def gcf_by_prime_factorization(self, nums: list) -> int:
        prime_factors_lists = []
        for num in nums:
            primes = PrimeFactorTree(num).primes
            prime_factors_lists.append(primes)

        common_factors = set(
            [p for primes in prime_factors_lists for p in primes])

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

        # If relatively prime, return 1, else gcf
        gcf = reduce(lambda x, y: x*y, occurrences) if occurrences else 1

        return gcf

    def get_algo_data(self, algorithm, nums: list):
        """Return gcf (int) and runtime (str) for a given GCF algorithm."""

        start = datetime.now()
        gcf = algorithm(nums)
        end = datetime.now()

        td = (end - start).total_seconds() * 10**3
        return gcf, f"{td:.03f}ms"

    def get_gcf_and_algo_runtimes(self, nums):
        """Return the GCF of the list of nums and the runtime of each
        implemented algorithm as a string."""

        gcf_values = {}
        runtimes = ""

        for name, algorithm in self.algos.items():
            gcf, runtime = self.get_algo_data(algorithm, nums)
            gcf_values[name] = gcf
            runtimes += f"{name} Algorithm runtime: {runtime}\n"

        self.bug_check(gcf_values)

        num_str = self.convert_nums_to_str(nums)
        gcf = list(gcf_values.values())[0]
        gcf = "1 (relatively prime)" if gcf == 1 else gcf
        results = f"{num_str}\nGCF: {gcf}\n{runtimes}"
        return results


def main():

    selections = {
        "1": ("Get GCF from user input of numbers", user_input),
        "2": ("Quick print sample GCFs", sample_data)}

    while True:
        for k, v in selections.items():
            print(f"{k}: {v[0]}")
        usr_in = input("Select function (q to quit): ").strip()
        if usr_in == "q":
            quit()
        elif usr_in in selections:
            print("")
            selections[usr_in][1]()
        else:
            print("Invalid selection.")


def sample_data():
    list_one = [18, 27]
    list_two = [20, 50, 120]
    list_three = [182664, 154875, 137688]
    # list_four = [182664, 1548787456, 1345877688, 849845486, 9848754542, 498498746546548]
    gcf_one = GCFCalculator(list_one).results
    print(gcf_one)
    gcf_two = GCFCalculator(list_two).results
    print(gcf_two)
    gcf_three = GCFCalculator(list_three).results
    print(gcf_three)
    # gcf_four = GCFCalculator(list_four).results
    # print(gcf_four)


def user_input():
    nums = []
    while True:
        try:
            usr_in = input(
                "Enter number (0 to finish entries): ").strip()
            if usr_in == "0":
                break
            nums.append(int(usr_in))
        except ValueError:
            print("Input must be an integer.")

    gcf_data = GCFCalculator(nums).results
    print(f"\n{gcf_data}")


if __name__ == "__main__":

    main()

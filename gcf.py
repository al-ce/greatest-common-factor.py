# References:
# https://www.calculatorsoup.com/calculators/math/gcf.php
# https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-euclidean-algorithm

from time import perf_counter_ns
from math import gcd, prod, sqrt
from functools import reduce


class GCFCalculator:

    def __init__(self, nums=[1, 1], tests=1):
        self.algorithms = self.get_algorithms_dict()
        self.results = self.get_gcf_and_algo_runtimes(nums, tests)

    def get_algorithms_dict(self):
        """Return a dict with {algorith name}, {algorith function} pairs."""

        algos = {
            "Euclidean": self.gcf_by_euclidean,
            "BinaryGCD": self.gcf_by_binary_algorithm,
            "Factoring": self.gcf_by_factoring,
            "PrimeFact": self.gcf_by_prime_factorization,
            "math.gcd ": self.gcf_by_math_gcd,
        }

        return algos

    def same_gcf_check(self, gcf_values: dict):
        """Raise an error if the algorithms return differing values."""

        gcfs = {gcf for gcf in gcf_values.values()}
        length = len(gcfs)

        if length == 1:
            return None

        msg = "Algorithms returned differing values.\n"

        for algorithm_name, gcf in gcf_values.items():
            msg += f"{algorithm_name} algorithm returned {gcf}\n"

        raise Exception(msg)

    def convert_nums_to_str(self, nums):
        """Convert a list of numbers to a csv string."""

        nums_str = "Numbers: " + ", ".join([str(num) for num in nums])

        return nums_str

    def factorization(self, n: int) -> list:
        """Get all the factors of an integer"""

        s = sqrt(n).__floor__()
        factors = [n]

        for i in range(2, s+1):
            q = n/i
            if q.is_integer():
                factors += [int(q), i]
        return factors

    def binary_gcd(self, a, b):
        # a, b = sorted([a, b], reverse=True)
        a, b = max([a, b]), min([a, b])

        if a == 0:
            return b
        elif b == 0:
            return a

        if a % 2 == 0:
            if b % 2 == 0:
                return 2 * self.binary_gcd(a >> 1, b >> 1)
            else:
                return self.binary_gcd(a >> 1, b)
        elif b % 2 == 0:
            return self.binary_gcd(a, b >> 1)
        else:
            return self.binary_gcd(abs(a-b) >> 1, b)

    def gcf_by_binary_algorithm(self, nums: list) -> int:
        """Get the GCF of a list of numbers with the binary GCD algorithm."""
        return reduce(self.binary_gcd, nums)

    def euclid(self, a, b):
        if a == 0:
            return b
        elif b == 0:
            return a

        r = a % b

        return self.euclid(b, r)  # def euclidean(nums):

    def gcf_by_euclidean(self, nums: list) -> int:
        """Get the GCF of a list of nums with the Euclidean Algorithm."""

        return reduce(self.euclid, nums)

    def gcf_by_factoring(self, nums: list) -> int:
        """Get the GCF of a list of nums by returning the max of their common factors."""

        factors_sets = []
        for num in nums:
            factors_sets.append(set(self.factorization(num)))

        common_factors = set.intersection(*factors_sets)

        gcf = max(common_factors) if common_factors else 1

        return gcf

    def is_prime(self, n):
        """Return True if n is prime, else return False."""

        for i in range(2, n//2):
            if (n % i) == 0:
                return False
        return True

    def prime_factorization(self, n: int, prime_factors: list):
        """Prime Factor Tree generator."""

        if self.is_prime(n):
            prime_factors.append(n)
            return n, prime_factors

        s = sqrt(n).__floor__()

        for i in range(2, s + 1):
            if n % i == 0:
                self.prime_factorization(i, prime_factors)
                self.prime_factorization(n//i, prime_factors)
                break

    def gcf_by_prime_factorization(self, nums: list) -> int:
        """Get the GCF of a list of nums by returning the product of their
        common prime factors multiplied by the highest occurence of these
        factors across all nums."""

        prime_factors_lists = []
        for num in nums:
            prime_factors = []
            self.prime_factorization(num, prime_factors)
            prime_factors_lists.append(prime_factors)

        common_factors = set(
            [p for primes in prime_factors_lists for p in primes])

        occurrences = []

        for p in common_factors:
            min_p = float('inf')
            for primes in prime_factors_lists:
                p_count = primes.count(p)
                min_p = min(min_p, p_count)

            # Add the highest number of occurrences of each prime factor
            # common to each number to the occurrences list
            occurrences.extend([p for i in range(min_p)])

        gcf = reduce(lambda x, y: x*y, occurrences) if occurrences else 1

        return gcf

    def gcf_by_math_gcd(self, nums: list) -> int:
        """Use Python's math.gcd function to  get the GCF of a list of nums."""

        return reduce(gcd, nums)

    def get_algo_data(self, algorithm: callable, nums: list, tests):
        """Return gcf (int) and runtime (str) for a given GCF algorithm. Run
        `tests` number of times and take the average."""

        runtimes = []
        for i in range(tests):

            # Measure runtime with perf_counter
            start = perf_counter_ns()

            gcf = algorithm(nums)

            end = perf_counter_ns()
            runtimes.append((end - start) / 1_000_000)

        td = (sum(runtimes) / tests)

        return gcf, f"{td:.5f}ms"

    def get_gcf_and_algo_runtimes(self, nums, tests):
        """Return the GCF of the list of nums and the runtime of each
        implemented algorithm as a string."""

        gcf_values = {}
        runtimes = ""

        for name, algorithm in self.algorithms.items():
            gcf, runtime = self.get_algo_data(algorithm, nums, tests)
            gcf_values[name] = gcf
            runtimes += f"  {name}: {runtime}\n"

        # Test that all functions returned the same value.
        self.same_gcf_check(gcf_values)

        num_str = self.convert_nums_to_str(nums)

        # We need to check the GCF returned by all the functinos is the same
        # to test for bugs in the functions, and if we've made it this far
        # without getting an error, the first item in gcf_values suffices.
        gcf = list(gcf_values.values())[0]
        gcf = "1 (relatively prime)" if gcf == 1 else gcf

        results = f"{num_str}\nGCF: {gcf}\nTests ran: {tests}\nAverage algorithm runtimes:\n{runtimes}"

        return results


class Test(GCFCalculator):
    def __init__(self):
        self.algos = self.get_algorithms_dict()

    def correct_result_check(self):
        """Check that each algorithm returns the same result as provided by the
        `math.gcd` method. This is a test run at program start, meant to go
        unnoticed by the user, to check that the algorithms have been
        implemented correctly."""

        # Expected GCFs: 3, 1, 1, 7, 9, 8, 2376, 10, 1
        numbers = [[64, 28], [3, 7], [19, 3, 7], [2, 3], [7, 21], [18, 27],
                   [72, 40], [33264, 35640], [120, 50, 20], [1, 20]]

        for nums in numbers:
            for name, algorithm in self.algos.items():

                algo_gcf = self.get_algo_data(algorithm, nums, 1)[0]

                # print(f"Nums: {nums} Name: {name} gcf {algo_gcf}")

                # math.gcd is presumably always correct, so we test against it
                py_math_gcd = gcd(*nums)

                if algo_gcf != py_math_gcd:
                    raise Exception(
                        f"{name} algorithm did not return the same result as math.gcd method\n"
                        f"Numbers:  {nums}\n"
                        f"Expected: {py_math_gcd}\nGot:      {algo_gcf}")


def main():
    # Run test on startup, raise exception if functions return incorrect GCF
    Test().correct_result_check()

    selections = {
        "1": ("Get GCF from user input of numbers", user_input),
        "2": ("Quick print sample GCFs", sample_data)}

    while True:

        [print(f"{k}: {v[0]}") for k, v in selections.items()]

        usr_in = input("Select function (q to quit): ").strip()

        if usr_in == "q":
            quit()
        elif usr_in in selections:
            tests = how_many_tests()
            print("")
            selections[usr_in][1](tests)
        else:
            print("Invalid selection.")


def sample_data(tests):
    """Print the GCF of pre-determined lists of nums, running all the
    implemented algos (see the .algos attr in the GCFCalculator class.)"""

    test_lists = [[3, 7], [18, 27], [20, 50, 120], [182664, 154875, 137688]]

    [print(GCFCalculator(num_list, tests).results) for num_list in test_lists]


def how_many_tests():
    """Ask user how many times to run each algorithm."""

    err = "Input must be a positive integer."
    while True:
        try:
            usr_in = input(
                "Number of times to run each algorithm (press <Enter> for once): ").strip()

            if usr_in == "":
                tests = 1
                break
            elif int(usr_in) < 1:
                print(err)
            else:
                tests = int(usr_in)
                break

        except ValueError:
            print(err)

    return tests


def user_input(tests):
    """Get numbers from user to calculate GCF."""

    nums = []
    err = "Input must be a positive integer."

    while True:
        try:
            usr_in = input(
                "Enter number (0 to finish entries): ").strip()

            if usr_in == "0":
                break
            elif int(usr_in) < 1:
                print(err)
            else:
                nums.append(int(usr_in))

        except ValueError:
            print(err)

    gcf_data = GCFCalculator(nums, tests).results
    print(f"\n{gcf_data}")


if __name__ == "__main__":

    main()

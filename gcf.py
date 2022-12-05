# References:
# https://www.calculatorsoup.com/calculators/math/gcf.php
# https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-euclidean-algorithm

from time import perf_counter_ns
from math import gcd, sqrt
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
        self.prime_factors = []
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
            self.prime_factors.append(n)
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
    def __init__(self, nums=[1, 1], tests=1):
        self.algos = self.get_algos_dict()
        self.results = self.get_gcf_and_algo_runtimes(nums, tests)

    def get_algos_dict(self):
        """Return a dict with {algorith name}, {algorith function} pairs."""

        algos = {
            "Euclidean": self.gcf_by_euclidean,
            "Factoring": self.gcf_by_factoring,
            "Prime Fct": self.gcf_by_prime_factorization,
        }

        return algos

    def same_gcf_check(self, gcf_values: dict):
        """Raise an error if the algorithms return differing values."""

        gcfs = {gcf for gcf in gcf_values.values()}
        length = len(gcfs)

        if length == 1:
            return None

        msg = "Algorithms returned differing values.\n"

        for algo_name, gcf in gcf_values.items():
            msg += f"{algo_name} algorithm returned {gcf}\n"

        raise Exception(msg)

    def convert_nums_to_str(self, nums):
        """Convert a list of numbers to a csv string."""

        nums_str = "Numbers:"

        for num in nums:
            nums_str += f" {num}"

        return nums_str

    def factorization(self, n: int) -> list:
        """Get all the factors of an integer"""

        s = sqrt(n).__floor__()  # call .__floor__ to round down
        factors = [n]

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
            nums = [a] + nums[2:]
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
        """Get the GCF of a list of nums by returning the max of their common factors."""

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
        """Get the GCF of a list of nums by returning the product of their
        common prime factors multiplied by the highest occurence of these
        factors across all nums."""

        # A list of lists - the nested lists are the list of prime factors
        prime_factors_lists = []

        for num in nums:
            # Get the list of all prime factors of num
            primes = PrimeFactorTree(num).prime_factors
            prime_factors_lists.append(primes)

        common_factors = set(
            [p for primes in prime_factors_lists for p in primes])

        occurrences = []

        for p in common_factors:
            min_p = float('inf')
            for primes in prime_factors_lists:
                # Count the occurrences of p for this list of prime factors
                p_count = primes.count(p)
                min_p = min(min_p, p_count)

            # Add the highest number of occurrences of each prime factor that is
            # common to each number to occurrences list
            occurrences.extend([p for i in range(min_p)])

        # If relatively prime, return 1, else gcf
        gcf = reduce(lambda x, y: x*y, occurrences) if occurrences else 1

        return gcf

    def get_algo_data(self, algorithm: callable, nums: list, tests):
        """Return gcf (int) and runtime (str) for a given GCF algorithm. Run
        `tests` number of times and take the average."""

        runtimes = []
        for i in range(tests):

            # Measure runtime with perf_counter
            start = perf_counter_ns()

            # algorith is a var for whatever func we passed
            gcf = algorithm(nums)

            end = perf_counter_ns()
            runtimes.append((end - start) / 1_000_000)

        td = (sum(runtimes) / tests)

        return gcf, f"avg {td:.03f}ms over {tests} tests"

    def get_gcf_and_algo_runtimes(self, nums, tests):
        """Return the GCF of the list of nums and the runtime of each
        implemented algorithm as a string."""

        gcf_values = {}
        runtimes = ""

        for name, algorithm in self.algos.items():
            gcf, runtime = self.get_algo_data(algorithm, nums, tests)
            gcf_values[name] = gcf
            runtimes += f"{name} algorithm runtime: {runtime}\n"

        # Test that all functions returned the same value.
        self.same_gcf_check(gcf_values)

        # Turn the list of ints into a single str
        num_str = self.convert_nums_to_str(nums)

        # We need to check the GCF returned by all the functinos is the same
        # to test for bugs in the functions, and if we've made it this far
        # without getting an error, the first item in gcf_values suffices.
        gcf = list(gcf_values.values())[0]
        gcf = "1 (relatively prime)" if gcf == 1 else gcf

        # Generate a message string with the results. If we need to get just
        # the GCF instead of the message string, we can get that from the
        # individual algorithm functions.
        results = f"{num_str}\nGCF: {gcf}\n{runtimes}"

        return results


class Test(GCFCalculator):
    def __init__(self):
        self.algos = self.get_algos_dict()

    def correct_result_check(self):
        """Check that each algorithm returns the same result as provided by the
        `math.gcd` method. This is a test run at program start, meant to go
        unnoticed by the user, to check that the algorithms have been
        implemented correctly."""

        # Expected GCFs: 3, 1, 1, 7, 9, 8, 2376, 10, 1
        numbers = [[3, 7], [19, 3, 7], [2, 3], [7, 21], [18, 27],
                   [72, 40], [33264, 35640], [120, 50, 20], [1, 20]]

        # Run each algorithm on each list of nums
        for nums in numbers:
            for name, algorithm in self.algos.items():

                algo_gcf = self.get_algo_data(algorithm, nums, 1)[0]
                # math.gcd is presumably always correct, so we test against it
                py_math_gcd = gcd(*nums)

                if algo_gcf != py_math_gcd:
                    raise Exception(
                        f"{name} algorithm did not return the same result as math.gcd method\n"
                        f"Numbers:  {nums}\n"\
                        f"Expected: {py_math_gcd}\nGot:      {algo_gcf}")


def main():
    # Run test on startup, raise exception if functions return incorrect GCF
    Test().correct_result_check()

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
            tests = how_many_tests()
            print("")
            selections[usr_in][1](tests)
        else:
            print("Invalid selection.")


def sample_data(tests):
    """Print the GCF of pre-determined lists of nums, running all the
    implemented algos (see the .algos attr in the GCFCalculator class.)"""

    list_one = [3, 7]
    list_two = [18, 27]
    list_three = [20, 50, 120]
    list_four = [182664, 154875, 137688]
    # list_five is quite large and takes a while to run
    # list_five = [182664, 1548787456, 1345877688, 849845486, 9848754542, 498498746546548]

    gcf_one = GCFCalculator(list_one, tests).results
    print(gcf_one)
    gcf_two = GCFCalculator(list_two, tests).results
    print(gcf_two)
    gcf_three = GCFCalculator(list_three, tests).results
    print(gcf_three)
    gcf_four = GCFCalculator(list_four, tests).results
    print(gcf_four)
    # gcf_five = GCFCalculator(list_five).results
    # print(gcf_five)


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

# :snake: greatest-common-factor.py

This is a CLI program written in Python to

1) Display the **GCF** (greatest common factor) of numbers in a list using various algorithms
2) Display the **runtime** of each algorithm.

Comparing the runtime of each algorithm is the more interesting part of this program, as Python's `math.gcd` function can get the GCF without all this implementation.



https://user-images.githubusercontent.com/23170004/205469921-06a6c7d9-232f-4d5e-bbc4-e02c6c636cbc.mp4


## Table of Contents
* [Why this program?](#question-why)
* [Usage](#beginner-usage)
    - [Manual number input](#pencil-manual-number-input)
    - [Sample lists](#ledger-sample-lists)
* [Implemented Algorithms](#pagewithcurl-implemented-algorithms)
* [Features](#features)
    - [Tests](#whitecheckmark-tests)
    - [Measurements](#triangularruler-measurements)
* [Results](#arrowright-results)
* [TODOs](#clock11-todos)

## :question: Why

I initially wanted a simple personal CLI tool to get the greatest common factor to check my work by hand, but I decided to make it a fun mini-project to practice some Python and math concepts.

## :beginner: Usage

No dependencies, just run `python gcf.py`.

The user has a choice of either `1)` manually inputting a list of numbers or `2)` running the program with some predetermined lists of numbers.
Next, the program will prompt the user to input a positive integer to determine how many times to run each algorithm on the list, so that the average runtime of each can be calculated more accurately (pressing `<Enter>` will pass the defaut `1`).
The lists will be passed to three algorithms, implemented from the descriptions at this [calculatorsoup.com](https://www.calculatorsoup.com/calculators/math/gcf.php) page.

### :pencil: Manual number input
After running `python gcf.py`, type `1` to manually input a list of numbers. 
The program will only accept integers, except for `q`, which quits the program.
The implemented `while` loop won't break until the user inputs `0`.

(Zero was chosen as the break-input since the GCF of any list of numbers containing zero must be the GCF of the same list without zero. Similarly, the GCF of any list of numbers containing 1 will be 1, but the program will accept this and run the algorithms anyway so we can still display the runtime, and the GCF displayed will also note that the numbers are [relatively prime](https://en.wikipedia.org/wiki/Coprime_integers))

### :ledger: Sample Lists
After running `python gcf.py`, type `2` to manually input a list of numbers.
The program displays the GCF of three lists of numbers. A fourth list with fairly large numbers is commented out in the `sample_data` function.

## :page_with_curl: Implemented Algorithms
- [Euclidean Algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm)
    - The `euclidean` function is called recursively on a pair of numbers. Python's built-in `reduce` function iterates over a list of numbers a pair at a time.
- [Binary GCD Algorithm](https://en.wikipedia.org/wiki/Binary_GCD_algorithm)
  - Implemented like the Euclidean algorithm, 
- Factoring
    - The `factorization` function generates a list of all the factors of `n` through trial division by checking if `n/i` in a range of `2` to `sqrt(n) + 1` (rounded down) is an int and appending the quotient to the list.
    - The `gcf_by_factoring` function returns the `max` of the intersection of the sets of each list of factors.
- [Prime factorization](https://www.calculatorsoup.com/calculators/math/prime-factors.php)
    - Using a binary tree of nodes with prime factor pairs, `gcf_by_prime_factorization` takes the list of primes provided by a binary tree of nodes with the prime factor pairs of a number.
    - The function returns the product of each common factor times the highest
      number of occurences of each factor in each number.


## Features

### :white_check_mark: Tests
* At start, the program initializes a dummy `Test` object before the user interface loads. `Test` is a child of the `GCFCalculator` class that runs all the algorithms. This `Test` object runs a `correct_results_check` function that calls every algorithm implemented by the `GCFCalculator` class as well as the Python `math` library's `gcd` method, passing some sample number lists to each of these. Assuming `math.gcd` is correctly calculating the GCF/D, we check that each algorithm is getting the same result. If it doesn't, the function raises an exception. This check allows us to make changes to existing algorithms or implement new ones without having to check the results by hand.





https://user-images.githubusercontent.com/23170004/205469673-a3b5cfc5-ad4d-485f-a36f-cafc3ae5a0a1.mov



* As a backup test, at the end of each check run by the user (manual or sample), a `same_gcf_check` checks the dict of GCFs returned by each algorithm. If the `set` of these values is of length > 1, then one or more of the algorithms returned a value different from the rest. The function raises an exception and displays what each algorithm returned.
  
  
  



https://user-images.githubusercontent.com/23170004/205469675-1789d443-f8ad-44c0-b933-0233085e9c17.mov



  
  This doesn't guarantee that any of the algorithms returned the *correct* result, but hopefully in tinkering or refactoring we only make a mistake on one of the algorithms at a time, so we can easily spot where that happened. This doesn't catch anything that wouldn't be caught by the `Test` object, assuming the `Test` object is being fed a similar test case on initilization as the case the user is inputting manually. But in case a bug is introduced to the `Test` object that goes un-noticed, this check gives us the benefit of telling us that *a*) there is a bug in one or more of our algorithms *b*) there is a bug in the `Test` object *c*) there is a special case the program hasn't accounted for.


### :triangular_ruler: Measurements
* Runtime measurements are calculated by getting the difference of `time.perf_counter()` at the start and end of each algorithm function call. Implementing a more rigourous method is on the TODOs.

## :arrow_right: Results

This is what the `sample_data` outputs on my machine after 150_000 tests:

```
Numbers: 18 27
GCF: 9
Euclidean algorithm runtime: avg 0.001ms over 150000 tests
Factoring algorithm runtime: avg 0.002ms over 150000 tests
Prime Fct algorithm runtime: avg 0.011ms over 150000 tests

Numbers: 20 50 120
GCF: 10
Euclidean algorithm runtime: avg 0.002ms over 150000 tests
Factoring algorithm runtime: avg 0.005ms over 150000 tests
Prime Fct algorithm runtime: avg 0.019ms over 150000 tests

Numbers: 182664 154875 137688
GCF: 3
Euclidean algorithm runtime: avg 0.004ms over 150000 tests
Factoring algorithm runtime: avg 0.079ms over 150000 tests
Prime Fct algorithm runtime: avg 0.176ms over 150000 tests
```

And after 1_000_000 tests:

```
Numbers: 18 27
GCF: 9
Euclidean algorithm runtime: avg 0.001ms over 1000000 tests
Factoring algorithm runtime: avg 0.002ms over 1000000 tests
Prime Fct algorithm runtime: avg 0.009ms over 1000000 tests

Numbers: 20 50 120
GCF: 10
Euclidean algorithm runtime: avg 0.002ms over 1000000 tests
Factoring algorithm runtime: avg 0.004ms over 1000000 tests
Prime Fct algorithm runtime: avg 0.015ms over 1000000 tests

Numbers: 182664 154875 137688
GCF: 3
Euclidean algorithm runtime: avg 0.003ms over 1000000 tests
Factoring algorithm runtime: avg 0.066ms over 1000000 tests
Prime Fct algorithm runtime: avg 0.154ms over 1000000 tests
```

## :clock11: TODOs

* Implement more algorithms.
* Replace the runtime measurement with something more rigorous and that can
  account for machine differences.
* Get advice on optimization, particularly for the `gcf_by_prime_factorization`
  function.

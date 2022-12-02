from datetime import datetime

# length = int(input("Input amount of numbers to check: "))
#
# nums = []
# for i in range(1, length+1):
#     num = int(input(f"Input a number ({i}/{length}): "))
#     nums.append(num)
#
# nums = sorted(nums, reverse=True)

nums = [182664, 154875, 137688]
# nums = [20, 50, 120]
# nums = [27, 18]


def euclidean(nums: list) -> int:
    # https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/the-euclidean-algorithm

    if len(nums) > 2:
        # Replace the first two nums in the list with their GCF
        a = euclidean(nums[0:2])
        nums = [a]+nums[2:]
        return euclidean(nums)

    a = nums[0]
    b = nums[1]
    print(f"A: {a}\nB: {b}")

    # If A = 0 then GCD(A,B)=B, since the GCD(0,B)=B, and we can stop.
    if a == 0:
        return b
    # If B = 0 then GCD(A,B)=A, since the GCD(A,0)=A, and we can stop.
    elif b == 0:
        return a

    q = round(a/b)  # quotient
    r = a % b       # remainder

    # Write A in quotient remainder form (A = B⋅Q + R)
    print(f"{a} = {b} * {q} + {r}\n")
    # Find GCD(B,R) using the Euclidean Algorithm since GCD(A,B) = GCD(B,R)
    return euclidean([b, r])  # def euclidean(nums):


algos = {
    "Euclidean": euclidean,
}


selection = "Euclidean"

start = datetime.now()
gcf = algos[selection](nums)
end = datetime.now()

print(f"{gcf}")

td = (end - start).total_seconds() * 10**3
print(f"Runtime of {selection} Algorithm: {td:.03f}ms")

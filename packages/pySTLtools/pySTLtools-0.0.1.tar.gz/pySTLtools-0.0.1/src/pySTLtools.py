
def count_set_bits(n):
	count=0
	while (n>0):
		count+=1
		n=n&(n-1)
	
	return count


def is_bit_set(n,i):
	#Checks if the i'th bit in the binary representation of a number n is set

	f=1
	f=f<<i
	if (n&f): return True
	else: return False




def primes_till_(ceiling):

    primality = dict([(i, False) for i in range(5, ceiling+1)])

    for x in range(1, int((ceiling)**0.5)+1):

        for y in range(1, int((ceiling)**0.5)+1):

            n = 4*x**2 + y**2

            if (n <= ceiling) and ((n % 12 == 1) or (n % 12 == 5)):
                primality[n] = not primality[n]

            n = 3*x**2 + y**2

            if (n <= ceiling) and (n % 12 == 7):
                primality[n] = not primality[n]

            n = 3*x**2 - y**2

            if (x > y) and (n <= ceiling) and (n % 12 == 11):
                primality[n] = not primality[n]

    for n in range(5, int((ceiling)**0.5)+1):

        if primality[n]:
            inde = 1

            while (inde * n**2 <= ceiling):
                primality[inde * n**2] = False
                inde += 1

    primes = []

    for i in range(ceiling + 1):
        if i in [0, 1, 4]: pass
        elif i in [2,3] or primality[i]: primes.append(i)
        else: pass
    return primes



# Problem description
I've written a diffie hellman server. I made sure not to let people select their parameters, and I use only strong primes. Those are safe, right?

# Challenge files/setup
Requires server.py, alice.py, auth.log are required. Including strong_primes and gen_agreed_primes.py is recommended, as it makes testing easier.

# The challenge
This is a diffie hellman server/client pair which uses a set of predetermined strong 2048-bit primes. An activity log is included that contains 256 authentications. The server generates a new ephemeral key for each session, but the client uses a static key, allowing for the vulnerability.

# Solution explanation
Because the protocol is using strong primes, and not safe primes, it is possible to retreive alice's static secret. To do this, you can extract a small prime factor from (p-1) for a large number of primes and run the pohlig-hellman method using them, rather than using the factors of any individual value of phi. Sagemath's trial_division function continues forever until it finds a factor, so it's better to use sage's EllitpicCurve class to do a lenstra factorization yourself with a max number of curves (10-25 is a good limit). Doing this gets about a 30 second running time. To further improve this, you can parallelize the solution pretty easily as I have, resulting in a sub 10-second running time.

# Correcting the flaw
This attack could be thwarted in a few ways. The first would be to use ephemeral keys on both ends. This is standard practice, as it provides forward secrecy. Using a single agreed-upon strong prime would work, though you could still extract a small portion of the key. You could also use safe primes instead of strong ones, as a safe prime only allows you to find the secret mod 2 (i.e. the least significant bit) through this method. The best way would be to use a single safe prime and use ephemeral keys on both ends, which is the standard procedure.
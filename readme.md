# Problem description
I've written a diffie hellman server. I made sure not to let people select their parameters, and I use only strong primes. Those are safe, right?

# Challenge files/setup
Requires server.py, alice.py, auth.log are required. Including strong_primes and gen_agreed_primes.py is recommended, as it makes testing easier.

# The challenge
This is a diffie hellman server/client pair which uses a set of predetermined strong 2048-bit primes. An activity log is included that contains 256 authentications. The server generates a new ephemeral key for each session, but the client uses a static key, allowing for the vulnerability.

# Solution explanation
Because the protocol is using strong primes, and not safe primes, it is possible to retreive alice's static secret. To do this, you can extract a small prime factor from (p-1) for a large number of primes. Sagemath's trial_division function extracts small factors fairly effectively, though ideally you would use a function that has a timeout built-in, in case the target has no small prime factors. I dealt with this problem by spinning off a new process for trial division, and then forcefully killing it after 3 seconds. Once you have these factors, you can then run the pohlig-hellman algorithm using the extracted factors to retreive alice's secret. My solution optimizes this a bit by checking after each factor if the secret is correct, and breaking the loop early if it is. My solution takes around 10 minutes or so, because trial division is pretty slow.

# Correcting the flaw
This attack could be thwarted in a few ways. The first would be to use ephemeral keys on both ends. This is standard practice, as it provides forward secrecy. Using a single agreed-upon strong prime would work, though you could still extract a small portion of the key. You could also use safe primes instead of strong ones, as a safe prime only allows you to find the secret mod 2 (i.e. the least significant bit) through this method. The best way would be to use a single safe prime and use ephemeral keys on both ends, which is the standard procedure.
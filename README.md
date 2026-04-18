# Delphi - Oracle Secret Brute Force

![web](https://img.shields.io/badge/topic-web-blue)
![oracle](https://img.shields.io/badge/type-oracle_attack-orange)
![bruteforce](https://img.shields.io/badge/technique-bruteforce-red)
![python](https://img.shields.io/badge/language-Python-grey)

---

## Overview.

This challenge presents a web application styled as a “mystical terminal” where users can interact with a set of commands. Among them, the `oracle` command hides a secret mechanism, it validates a user-supplied string and reveals a prophecy only if the correct secret is provided.

Despite the mystical theme, the backend logic exposes a classic vulnerability, a **prefix-based oracle**, which allows an attacker to reconstruct the secret **character by character** through differential responses.

---

## Challenge Description.

> These modern day shamans have created a website, can you learn their secret and be able to use magic yourself?

* **Website:** [http://url-of-the.chall/](http://url-of-the.chall/) (not the real one)
* **Flag format:** `ptm{...}`

---

## The vulnerability.

The `/secret` endpoint behaves differently depending on the correctness of the input:

* Incorrect input → `"Wrong secret :("`.
* Partially correct prefix → *Different response*.
* Fully correct secret → returns the **flag (prophecy)**.

This creates a **side-channel leak**:

> The server reveals whether a given input is a *correct prefix* of the secret.

This turns the problem into a deterministic brute force instead of guessing the entire string.

---

## Exploitation strategy.

Instead of brute forcing the whole secret at once, we:

1. Start with an empty string.
2. Try all possible characters (`a-z` + `_`) for the next position.
3. Send each candidate to the oracle.
4. Detect if the response changes (i.e., not `"Wrong secret :("`).
5. If it does → the character is correct.
6. Repeat until the full secret is recovered.

This reduces complexity dramatically:

* From **O(n^k)** → to **O(n × charset)**

---

## Example attack flow.

```
secret = ""

Try: "a" → Wrong.
Try: "b" → Wrong.
...
Try: "m" → Different response.

secret = "m"
```

Continue:

```
"ma" → ok.
"mag" → ok.
...
```

Eventually reconstruct:

```
magic_is_fake
```

---

## Final result.

* **Recovered secret:** `magic_is_fake`
* **Flag:** `ptm{l3t5_g0_t0_gr33c3}`

---

## Exploit script.

The included script automates the attack:

```bash
pip install requests
python solve.py
```

### Key logic:

```python
if "Wrong secret" not in resp.text:
    secret += c
```

The script detects when a prefix is correct and builds the secret incrementally.

---

## Why this works.

This is a classic **oracle vulnerability**, where:

* The server leaks information about internal state.
* Responses differ based on partial correctness.
* No rate limiting or protections are applied.

Such flaws are common in:

* Authentication systems.
* API key validation.
* Cryptographic padding oracles.

---

## How to fix it.

To prevent this class of attacks:

* Always return **constant responses** for invalid inputs.
* Avoid leaking information about *partial correctness*.
* Implement **rate limiting**.
* Use **constant-time comparisons** for secrets.
* Add monitoring for repeated automated requests.

---

## Files.

* `solve.py` → Python script to brute force the secret.
* `writeup.txt` → Detailed step-by-step solution.

---

## Takeaway.

Even simple applications can hide subtle vulnerabilities.
If an attacker can distinguish between *“wrong”* and *“almost right”*, the secret is already halfway compromised.

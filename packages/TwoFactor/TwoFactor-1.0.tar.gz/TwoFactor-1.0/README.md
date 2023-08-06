# TwoFactor

![Image](https://auth0.com/learn/wp-content/uploads/2016/03/tfa-what.png)

#### TwoFactor is a [2FA](https://en.wikipedia.org/wiki/Multi-factor_authentication) library  that allows:
[Buy me a coffee ☕︎](https://paywall.link/to/donate)

- [x] Generate secretkey.
- [x] Generate 2FA code.
- [x] Check code 2FA.

## Instalation

##### (TwoFactor)  requires [ Python ](https://www.python.org) v3.8

```sh
$ pip install TwoFactor
```

#### Getting Started

```python
Python 3.8.3 (default, Jun 16 2020, 19:00:28)
[GCC 6.3.0 20170516] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import TwoFactor
>>>
>>> TwoFactor = TwoFactor.TwoFactor()
```

#### Generate Secret

```python
>>> Secret = TwoFactor.getsecret() # Generates only one key.
>>> Secret
'ZD5EAENN4XBDTC25'
>>>
>>> Secrets = TwoFactor.getsecrets(5) # Generates a specified number of keys.
>>> Secrets
['T5CANGZTCQEPGRAF', 'OCBNMTJLBOQASEHD', 'BGL7TQ4AX34QB6YT', 'XHUI6P7HRV4KSEFI', 'HKAFBDYW6FBH6W47']
```

#### Generate Code

```python
>>> Code = TwoFactor.getcode(Secret)
>>> Code
895144
>>>
>>> Codes = TwoFactor.getcodes(Secrets)
>>> Codes 
{'T5CANGZTCQEPGRAF': '212242', 'OCBNMTJLBOQASEHD': '301778', 'BGL7TQ4AX34QB6YT': '367756', 'XHUI6P7HRV4KSEFI': '982273', 'HKAFBDYW6FBH6W47': '585889'}
```

#### Check Code 2FA.

```python
>>> CheckCode2Fa = TwoFactor.checkcode2fa(Secret, Code)
>>> CheckCode2Fa
True
>>>
```




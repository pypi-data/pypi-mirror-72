# Transliteration-BruteForcer

## How to
### Example
```python
>>> from transliteration_brute_forcer import TransliterationBruteForcer
>>> transliteration_bruteforcer = TransliterationBruteForcer()
>>> transliteration_bruteforcer.run('Юрий')
{'Urij'}
>>> transliteration_bruteforcer.custom_mapping = {
...     'Ю': ['Yu', 'Iy'],
...     'ю': ['yu', 'iy'],
...     'й': ['ii', 'iy', 'yy', 'yu'],
... }
>>> transliteration_bruteforcer.run('Юрий')
{'Urij', 'Yuriyu', 'Iyrij', 'Uriyy', 'Yuriii', 'Iyriii', 'Iyriyy', 'Uriiy', 'Yuriyy', 'Iyriyu', 'Uriyu', 'Iyriiy', 'Yurij', 'Uriii', 'Yuriiy'}
>>> transliteration_bruteforcer.run('Владимир Пехтин')
{'Vladimir Pehtin'}
>>> transliteration_bruteforcer.custom_mapping['х'] = ['kh']
>>> transliteration_bruteforcer.run('Владимир Пехтин')
{'Vladimir Pehtin', 'Vladimir Pekhtin'}
>>> transliteration_bruteforcer.custom_mapping['В'] = ['W']
>>> transliteration_bruteforcer.run('Владимир Пехтин')
{'Vladimir Pekhtin', 'Vladimir Pehtin', 'Wladimir Pekhtin', 'Wladimir Pehtin'}
```

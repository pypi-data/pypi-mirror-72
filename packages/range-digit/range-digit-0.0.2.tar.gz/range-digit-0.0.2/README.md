## description

`range-digit` is library of decimal digit which has `low` and `sup`.

```
d = RangeDigit('1.240')
print(d)  # 1.240
print(d - Decimal(1.2))  # 0.040
print(d / 2)  # 0.620
print(d.low)  # 1.2395
print(d.sup)  # 1.2405
print(d.tostr())  # <RangeDigit [1.2395 - 1.2405)>
```
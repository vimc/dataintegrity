import utils
import decimal

array1withnulls = [435621, "text", False, decimal.Decimal('NAN'), None]
array2withnulls = [435621, "text", False, decimal.Decimal('NAN'), None]
array3withnulls = [435622, "text", False, decimal.Decimal('NAN'), None]

print("comparing equal arrays")
if utils.ARRAYEQUAL(array1withnulls, array2withnulls):
    print("success")
else:
    print("fail")

print("comparing different arrays")
if utils.ARRAYEQUAL(array1withnulls, array3withnulls):
    print("fail")
else:
    print("success")
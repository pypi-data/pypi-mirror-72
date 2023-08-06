# Package: generalvector
Vectors made by me, featuring Vec and Vec2, inspired by Expression 2* in Wiremod inside Garry's Mod. 

The vectors are immutable, so any time a value inside one is changed it returns a new vector.

The bulk of the code is written twice, with one verion in vector and one version in vector2. I've begun adding new functions into general instead which both vectors inherit from, to make the code DRY. The General class can take an arbitrary amount of axis which allows us to easily add, for example, a Vec4 in the future if all code is moved to general.

*https://github.com/wiremod/wire/wiki/Expression-2


## Installation
```
pip install generalvector
```

## Usage example
```python
from generalvector import Vec, Vec2
assert Vec(3) + 2 == Vec(5, 5, 5)
assert Vec2(3, 4).length() == 5
```
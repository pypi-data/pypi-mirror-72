
# Interspace
Gives us different distance between two vectors which are given in as an input.

## Installation

```bash
pip install interspace
```

## Different Distance Functions

- [Minkowski distance(p-Norm Distance)](https://en.wikipedia.org/wiki/Minkowski_distance)
>minkowski(vector_1, vector_2, p=1)
- [Euclidean distance (2-norm distance)](https://en.wikipedia.org/wiki/Euclidean_distance)
>euclidean(vector_1, vector_2)
-  [Manhattan distance/Taxicab norm](https://en.wikipedia.org/wiki/Taxicab_geometry)
>manhattan(vector_1, vector_2)
- [Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)
>cosine_similarity(vector_1, vector_2)
- [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula)
>haversine(coord1, coord2, R = 6372800)
- [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance)
>hamming(int, int)

>hamming(str, str) # where, length of both the strings should be same

## Usage

```python
import interspace

# Calculate Euclidean Distace
interspace.euclidean([1,2,3],[4,5,6])
##Output: 5.196152422706632

# Compute the great-circle distance between two points on a sphere 
# given their longitudes and latitudes.
interspace.haversine((42.5170365,  15.2778599),(51.5073219,  -0.1276474))
##Output: 1532329.6237517272
```
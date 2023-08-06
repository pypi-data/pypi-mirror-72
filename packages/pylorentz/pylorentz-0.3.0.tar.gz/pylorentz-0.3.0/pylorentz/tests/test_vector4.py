""" Unittests for the class Vector4
"""

import unittest
import numpy as np
import cmath
import math
from pylorentz import Vector4, Momentum4


class Vector4TestCase(unittest.TestCase):
    """
    Test the implementation of Vector4.
    """

    def test_repr(self):
        """
        Check that the representation returns a string that recreates the
        object.
        """
        vec = Vector4(1, 2, 3, 4)
        self.assertEqual(repr(vec), "Vector4(1, 2, 3, 4)")

    def test_repr_vectorized(self):
        """
        Check that the representation returns a string that recreates the
        object.
        """
        x1 = np.array([1, 2, 3, 5])
        x2 = np.array([1, 2, 3, 6])
        x3 = np.array([1, 2, 3, 7])
        x4 = np.array([1, 2, 3, 8])
        vec = Vector4(x1, x2, x3, x4)

        self.assertEqual(repr(vec), "Vector4("
            "array([1, 2, 3, 5]), "
            "array([1, 2, 3, 6]), "
            "array([1, 2, 3, 7]), "
            "array([1, 2, 3, 8]))")

    def test_init_numbers(self):
        """
        Check that objects can be created using four values.
        """
        vec = Vector4(1, 2, 3, 4)
        self.assertEqual(list(vec._values), [1, 2, 3, 4])
        self.assertIsInstance(vec._values, np.ndarray)

    def test_init_not_four(self):
        """
        Check that init raises an error if the number of arguments is not
        four.
        """
        self.assertRaises(TypeError, Vector4, 1, 2, 3)
        self.assertRaises(TypeError, Vector4, 1, 2, 3, 4, 5)

    def test_init_copy(self):
        """
        Check that objects can be copied.
        """
        vec = Vector4(1, 2, 3, 4)
        vec2 = Vector4(vec)

        vec._values = [0, 0, 0, 0]

        self.assertEqual(list(vec._values), [0, 0, 0, 0])
        self.assertEqual(list(vec2._values), [1, 2, 3, 4])

    def test_init_vectorized(self):
        """
        Check that numpy arrays can be used as components
        """
        x1 = np.array([1, 2, 3, 5])
        x2 = np.array([1, 2, 3, 6])
        x3 = np.array([1, 2, 3, 7])
        x4 = np.array([1, 2, 3, 8])

        vec = Vector4(x1, x2, x3, x4)
        self.assertEqual(list(vec._values[0]), list(x1))
        self.assertEqual(list(vec._values[1]), list(x2))
        self.assertEqual(list(vec._values[2]), list(x3))
        self.assertEqual(list(vec._values[3]), list(x4))

    def test_add(self):
        """
        Check that two 4-vectors can be added.
        """
        vec = Vector4(1, 2, 3, 4)
        vec2 = Vector4(3, 4, 5, 10)

        self.assertEqual(str(vec + vec2),
                         "Vector4(4, 6, 8, 14)") 

    def test_add_vectorized(self):
        """
        Check that numpy arrays can be used in additions.
        """
        x1 = np.array([1, 2, 3, 5])
        x2 = np.array([1, 2, 3, 6])
        x3 = np.array([1, 2, 3, 7])
        x4 = np.array([1, 2, 3, 8])

        vec = Vector4(x1, x2, x3, x4)
        vec2 = Vector4(6, 7, 8, 9)

        sum = vec + vec2
        self.assertEqual(list(sum._values[0]), [7, 9, 11, 14])
        self.assertEqual(list(sum._values[1]), [7, 9, 11, 15])
        self.assertEqual(list(sum._values[2]), [7, 9, 11, 16])
        self.assertEqual(list(sum._values[3]), [7, 9, 11, 17])

        y1 = np.array([2, 2, 3, 5])
        y2 = np.array([2, 2, 3, 6])
        y3 = np.array([2, 2, 3, 7])
        y4 = np.array([2, 2, 3, 8])
        vec2 = Vector4(y1, y2, y3, y4)

        sum = vec + vec2
        self.assertEqual(list(sum._values[0]), [3, 4, 6, 10])
        self.assertEqual(list(sum._values[1]), [3, 4, 6, 12])
        self.assertEqual(list(sum._values[2]), [3, 4, 6, 14])
        self.assertEqual(list(sum._values[3]), [3, 4, 6, 16])

    def test_add_types(self):
        """
        Check that a 4-vectors and numbers cannot be added.
        """
        vec = Vector4(1, 2, 3, 4)
        self.assertRaises(TypeError, lambda: vec + 4)

    def test_iadd(self):
        """
        Check that two 4-vectors can be added in-place.
        """
        vec = Vector4(1, 2, 3, 4)
        vec2 = Vector4(3, 4, 5, 10)

        vec2 += vec

        self.assertEqual(str(vec2), "Vector4(4, 6, 8, 14)") 

    def test_iadd_types(self):
        """
        Check that a 4-vectors and numbers cannot be added in-place.
        """
        def func1():
            vec = Vector4(1, 2, 3, 4)
            vec += 4

        self.assertRaises(TypeError, func1)

    def test_iadd_vectorized_right(self):
        """
        Check that numpy arrays can be in-place added from the right.
        """
        x1 = np.array([1, 2, 3, 5])
        x2 = np.array([1, 2, 3, 6])
        x3 = np.array([1, 2, 3, 7])
        x4 = np.array([1, 2, 3, 8])

        vec = Vector4(x1, x2, x3, x4)
        vec2 = Vector4(6, 7, 8, 9)

        vec2 += vec

        self.assertEqual(list(vec2._values[0]), [7, 9, 11, 14])
        self.assertEqual(list(vec2._values[1]), [7, 9, 11, 15])
        self.assertEqual(list(vec2._values[2]), [7, 9, 11, 16])
        self.assertEqual(list(vec2._values[3]), [7, 9, 11, 17])

    def test_iadd_vectorized_left(self):
        """
        Check that numpy arrays can be in-place added from the left.
        """
        x1 = np.array([1, 2, 3, 5])
        x2 = np.array([1, 2, 3, 6])
        x3 = np.array([1, 2, 3, 7])
        x4 = np.array([1, 2, 3, 8])

        vec = Vector4(x1, x2, x3, x4)
        vec2 = Vector4(6, 7, 8, 9)

        vec += vec2

        self.assertEqual(list(vec._values[0]), [7, 9, 11, 14])
        self.assertEqual(list(vec._values[1]), [7, 9, 11, 15])
        self.assertEqual(list(vec._values[2]), [7, 9, 11, 16])
        self.assertEqual(list(vec._values[3]), [7, 9, 11, 17])

    def test_iadd_vectorized_both(self):
        """
        Check that two numpy arrays can be in-place.
        """
        x1 = np.array([1, 2, 3, 5])
        x2 = np.array([1, 2, 3, 5])
        x3 = np.array([1, 2, 3, 7])
        x4 = np.array([1, 2, 3, 8])

        vec = Vector4(x1, x2, x3, x4)
        vec2 = Vector4(x4, x3, x2, x1)

        vec += vec2

        self.assertEqual(list(vec._values[0]), [2, 4, 6, 13])
        self.assertEqual(list(vec._values[1]), [2, 4, 6, 12])
        self.assertEqual(list(vec._values[2]), [2, 4, 6, 12])
        self.assertEqual(list(vec._values[3]), [2, 4, 6, 13])

    def test_sub(self):
        """
        Check that two 4-vectors can be subtracted.
        """
        vec = Vector4(1, 2, 3, 4)
        vec2 = Vector4(3, 4, 5, 10)

        self.assertEqual(str(vec - vec2),
                         "Vector4(-2, -2, -2, -6)") 

    def test_sub_vectorized(self):
        """
        Check that numpy arrays can be used in differences.
        """
        x1 = np.array([1, 2, 3, 5])
        x2 = np.array([1, 2, 3, 6])
        x3 = np.array([1, 2, 3, 7])
        x4 = np.array([1, 2, 3, 8])

        vec = Vector4(x1, x2, x3, x4)
        vec2 = Vector4(6, 2, 1, 0)

        sum = vec - vec2
        self.assertEqual(list(sum._values[0]), [-5, 0, 2, 5])
        self.assertEqual(list(sum._values[1]), [-5, 0, 2, 6])
        self.assertEqual(list(sum._values[2]), [-5, 0, 2, 7])
        self.assertEqual(list(sum._values[3]), [-5, 0, 2, 8])

        y1 = np.array([2, 2, 3, 5])
        y2 = np.array([2, 2, 3, 1])
        y3 = np.array([2, 2, 3, 2])
        y4 = np.array([2, 2, 3, 0])
        vec2 = Vector4(y1, y2, y3, y4)

        sum = vec - vec2
        self.assertEqual(list(sum._values[0]), [-1, 0, 0, 0])
        self.assertEqual(list(sum._values[1]), [-1, 0, 0, 5])
        self.assertEqual(list(sum._values[2]), [-1, 0, 0, 5])
        self.assertEqual(list(sum._values[3]), [-1, 0, 0, 8])

    def test_sub_types(self):
        """
        Check that a 4-vectors and numbers cannot be subtracted.
        """
        vec = Vector4(1, 2, 3, 4)
        self.assertRaises(TypeError, lambda: vec - 4)

    def test_isub(self):
        """
        Check that two 4-vectors can be subtracted in-place.
        """
        vec = Vector4(1, 2, 3, 4)
        vec2 = Vector4(3, 4, 5, 10)

        vec -= vec2

        self.assertEqual(str(vec), "Vector4(-2, -2, -2, -6)") 

    def test_isub_types(self):
        """
        Check that a 4-vectors and numbers cannot be subtracted in-place.
        """
        def func2():
            vec = Vector4(1, 2, 3, 4)
            vec -= 4

        self.assertRaises(TypeError, func2)

    def test_isub_vectorized_right(self):
        """
        Check that numpy arrays can be used in in-place differences from the
        right.
        """
        x1 = np.array([1, 2, 3, 5])
        x2 = np.array([1, 2, 3, 6])
        x3 = np.array([1, 2, 3, 7])
        x4 = np.array([1, 2, 3, 8])

        vec = Vector4(x1, x2, x3, x4)
        vec2 = Vector4(3, 2, 0, 9)

        vec2 -= vec

        self.assertEqual(list(vec2._values[0]), [2, 0, -3, 4])
        self.assertEqual(list(vec2._values[1]), [2, 0, -3, 3])
        self.assertEqual(list(vec2._values[2]), [2, 0, -3, 2])
        self.assertEqual(list(vec2._values[3]), [2, 0, -3, 1])

    def test_isub_vectorized_left(self):
        """
        Check that numpy arrays can be used in in-place differences from the
        left.
        """
        x1 = np.array([1, 2, 3, 5])
        x2 = np.array([1, 2, 3, 6])
        x3 = np.array([1, 2, 3, 7])
        x4 = np.array([1, 2, 3, 8])

        vec = Vector4(x1, x2, x3, x4)
        vec2 = Vector4(3, 2, 0, 9)

        vec -= vec2

        self.assertEqual(list(vec._values[0]), [-2, 0, 3, -4])
        self.assertEqual(list(vec._values[1]), [-2, 0, 3, -3])
        self.assertEqual(list(vec._values[2]), [-2, 0, 3, -2])
        self.assertEqual(list(vec._values[3]), [-2, 0, 3, -1])

    def test_isub_vectorized_both(self):
        """
        Check that two numpy arrays can be used in in-place differences.
        """
        x1 = np.array([1, 2, 5])
        x2 = np.array([1, 2, 5])
        x3 = np.array([1, 2, 7])
        x4 = np.array([1, 2, 8])

        vec = Vector4(x1, x2, x3, x4)
        vec2 = Vector4(x4, x3, x2, x1)

        vec -= vec2

        self.assertEqual(list(vec._values[0]), [0, 0, -3])
        self.assertEqual(list(vec._values[1]), [0, 0, -2])
        self.assertEqual(list(vec._values[2]), [0, 0, 2])
        self.assertEqual(list(vec._values[3]), [0, 0, 3])

    def test_mul_scalar(self):
        """
        Check that multiplying the vector by a scalar, scales the vector.
        """
        x1 = np.array([1, 2, 5])
        x2 = np.array([1, 2, 5])
        x3 = np.array([1, 2, 7])
        x4 = np.array([1, 2, 8])
        vec = Vector4(x1, x2, x3, x4)

        vec = vec * 2

        self.assertEqual(list(vec._values[0]), [2, 4, 10])
        self.assertEqual(list(vec._values[1]), [2, 4, 10])
        self.assertEqual(list(vec._values[2]), [2, 4, 14])
        self.assertEqual(list(vec._values[3]), [2, 4, 16])

    def test_mul_scalar_vectorized(self):
        """
        Check that multiplying a numpy-vector by a scalar works.
        """
        vec = Vector4(1, 0, 4, 5)

        self.assertEqual(str(vec * 2), 'Vector4(2, 0, 8, 10)')

    def test_mul_dot_product(self):
        """
        Check that multiplying two vectors, returns the dot product.
        """
        vec = Vector4(2, 0, 4, 5)
        vec2 = Vector4(7, 0, -1, 3)

        self.assertEqual(vec * vec2, 14 - 0 + 4 - 15)

    def test_mul_dot_product_vectorized_left(self):
        """
        Check that multiplying two vectors (the left a numpy array), returns
        an array of dot products.
        """
        x1 = np.array([1, 2, 5])
        x2 = np.array([1, 2, 5])
        x3 = np.array([1, 2, 7])
        x4 = np.array([1, 2, 8])
        vec = Vector4(x1, x2, x3, x4)
        vec2 = Vector4(7, 0, -1, 3)

        products = vec * vec2
        self.assertEqual(list(products), [5, 10, 5*7 + 7 - 3*8])

    def test_mul_dot_product_vectorized_right(self):
        """
        Check that multiplying two vectors (the right a numpy array), returns
        an array of dot products.
        """
        x1 = np.array([1, 2, 5])
        x2 = np.array([1, 2, 5])
        x3 = np.array([1, 2, 7])
        x4 = np.array([1, 2, 8])
        vec = Vector4(x1, x2, x3, x4)
        vec2 = Vector4(7, 0, -1, 3)

        products = vec2 * vec
        self.assertEqual(list(products), [5, 10, 5*7 + 7 - 3*8])

    def test_mul_dot_product_vectorized_both(self):
        """
        Check that multiplying two numpy vectors returns an array of dot
        products.
        """
        x1 = np.array([1, 2, 5])
        x2 = np.array([1, 2, 5])
        x3 = np.array([1, 2, 7])
        x4 = np.array([1, 2, 8])
        vec = Vector4(x1, x2, x3, x4)
        vec2 = Vector4(x3, x4, x1, x2)

        products = vec * vec2
        self.assertEqual(list(products), [-2, -8, -80])

    def test_rmul_scalar(self):
        """
        Check that multiplying the vector by a scalar from left, scales the vector.
        """
        vec = Vector4(1, 0, 4, 5)
        self.assertEqual(str(2 * vec), 'Vector4(2, 0, 8, 10)')

    def test_rmul_scalar_vectorized(self):
        """
        Check that multiplying the numpy vector by a scalar from left, scales the vector.
        """
        x1 = np.array([1, 2, 5])
        x2 = np.array([1, 2, 5])
        x3 = np.array([1, 2, 7])
        x4 = np.array([1, 2, 8])
        vec = Vector4(x1, x2, x3, x4)

        vec = 2 * vec
        self.assertEqual(list(vec._values[0]), [2, 4, 10])
        self.assertEqual(list(vec._values[1]), [2, 4, 10])
        self.assertEqual(list(vec._values[2]), [2, 4, 14])
        self.assertEqual(list(vec._values[3]), [2, 4, 16])

    def test_imul_scalar(self):
        """
        Check that multiplying a vector by a scaler in-place, scales the vector.
        """
        vec = Vector4(1, 0, 4, 5)
        vec *= 2

        self.assertEqual(str(vec), 'Vector4(2, 0, 8, 10)')

    def test_imul_scalar_vectorized(self):
        """
        Check that multiplying a numpy vector by a scaler in-place, scales the vector.
        """
        x1 = np.array([1, 2, 5])
        x2 = np.array([1, 2, 5])
        x3 = np.array([1, 2, 7])
        x4 = np.array([1, 2, 8])
        vec = Vector4(x1, x2, x3, x4)

        vec *= 2

        self.assertEqual(list(vec._values[0]), [2, 4, 10])
        self.assertEqual(list(vec._values[1]), [2, 4, 10])
        self.assertEqual(list(vec._values[2]), [2, 4, 14])
        self.assertEqual(list(vec._values[3]), [2, 4, 16])

    def test_imul_dot_product(self):
        """
        Check that multiplying a vector by a vector in-place, raises an error.
        """
        def func3():
            vec = Vector4(2, 0, 4, 5)
            vec2 = Vector4(7, 0, -1, 3)

            vec *= vec2

        self.assertRaises(TypeError, func3)

    def test_neg(self):
        """
        Check that negating the vector is equivalent to multiplication with
        -1.
        """
        vec = Vector4(-2, 0, -8, -10)

        self.assertEqual(str(-vec), 'Vector4(2, 0, 8, 10)')

    def test_neg_vectorized(self):
        """
        Check that negating the vector is equivalent to multiplication with
        -1.
        """
        x1 = np.array([-2, -4, -10])
        x2 = np.array([-2, -4, -10])
        x3 = np.array([-2, -4, -14])
        x4 = np.array([-2, -4, -16])

        vec = -Vector4(x1, x2, x3, x4)

        self.assertEqual(list(vec._values[0]), [2, 4, 10])
        self.assertEqual(list(vec._values[1]), [2, 4, 10])
        self.assertEqual(list(vec._values[2]), [2, 4, 14])
        self.assertEqual(list(vec._values[3]), [2, 4, 16])

    def test_div_scalar(self):
        """
        Check that dividing a vector by a scalar, scales the vector.
        """
        vec = Vector4(1, 0, 4, 5)
        self.assertEqual(str(vec / 2.0), 'Vector4(0.5, 0, 2, 2.5)')

    def test_div_scalar_vectorized(self):
        """
        Check that dividing a numpy vector by a scalar, scales the vector.
        """
        x1 = np.array([1, 2, 5])
        x2 = np.array([1, 2, 5])
        x3 = np.array([1, 2, 7])
        x4 = np.array([1, 2, 8])
        vec = Vector4(x1, x2, x3, x4)

        vec = vec / 2.0

        self.assertEqual(list(vec._values[0]), [0.5, 1, 2.5])
        self.assertEqual(list(vec._values[1]), [0.5, 1, 2.5])
        self.assertEqual(list(vec._values[2]), [0.5, 1, 3.5])
        self.assertEqual(list(vec._values[3]), [0.5, 1, 4])

    def test_floordiv_scalar(self):
        """
        Check that dividing a vector by a scalar, scales the vector.
        """
        vec = Vector4(1, 0, 4, 5)
        self.assertEqual(str(vec // 3), 'Vector4(0, 0, 1, 1)')

    def test_ifloordiv_scalar(self):
        """
        Check that dividing a vector by a scalar in-place, scales the vector.
        """
        vec = Vector4(1, 0, 4, 5)
        vec //= 3
        self.assertEqual(str(vec), 'Vector4(0, 0, 1, 1)')

    def test_div_types(self):
        """
        Check that dividing two vectors, raises an exception.
        """
        vec = Vector4(2, 0, 4, 5)
        vec2 = Vector4(7, 0, -1, 3)

        self.assertRaises(TypeError, lambda: vec / vec2)

    def test_floordiv_types(self):
        """
        Check that dividing two vectors, raises an exception.
        """
        vec = Vector4(2, 0, 4, 5)
        vec2 = Vector4(7, 0, -1, 3)

        self.assertRaises(TypeError, lambda: vec // vec2)

    def test_rdiv_scalar(self):
        """
        Check that dividing a scalar by vector raises an exception.
        """
        vec = Vector4(1, 0, 4, 5)
        self.assertRaises(TypeError, lambda: 1 / vec)

    def test_rdiv_types(self):
        """
        Check that dividing two vectors raises an exception.
        """
        vec = Vector4(1, 0, 4, 5)
        vec2 = Vector4(1, 0, 4, 5)
        self.assertRaises(TypeError, lambda: vec2 / vec)

    def test_idiv_types(self):
        """
        Check that dividing a vector by a vector in-place, raises an error.
        """
        def func4():
            vec = Vector4(2, 0, 4, 5)
            vec2 = Vector4(7, 0, -1, 3)

            vec /= vec2

        self.assertRaises(TypeError, func4)

    def test_idiv_scalar(self):
        """
        Check that dividing a vector by a scalar in-place, scales the vector.
        """
        vec = Vector4(1, 0, 4, 5)
        vec /= 2.0

        self.assertEqual(str(vec), 'Vector4(0.5, 0, 2, 2.5)')

    def test_idiv_scalar_vectorized(self):
        """
        Check that dividing a numpy vector by a scalar in-place, scales the vector.
        """
        x1 = np.array([1, 2, 5])
        x2 = np.array([1, 2, 5])
        x3 = np.array([1, 2, 7])
        x4 = np.array([1, 2, 8])
        vec = Vector4(x1, x2, x3, x4)

        vec /= 2.0

        self.assertEqual(list(vec._values[0]), [0.5, 1, 2.5])
        self.assertEqual(list(vec._values[1]), [0.5, 1, 2.5])
        self.assertEqual(list(vec._values[2]), [0.5, 1, 3.5])
        self.assertEqual(list(vec._values[3]), [0.5, 1, 4])

    def test_mag(self):
        """
        Check that mag returns the magnitude of the vectors respecting the
        metric.
        """
        vec = Vector4(4, 0, 3, 4)
        self.assertEqual(vec.mag, 3j)

        vec = Vector4(7, 2, 3, 4)
        self.assertEqual(vec.mag, cmath.sqrt(49 - 4 - 9 - 16))

    def test_mag_vectorized(self):
        """
        Check that mag returns the magnitude of the numpy vectors respecting
        the metric.
        """
        x1 = np.array([1, 2, 5])
        x2 = np.array([1, 2, 5])
        x3 = np.array([1, 2, 7])
        x4 = np.array([1, 2, 8])
        vec = Vector4(x1, x2, x3, x4)

        self.assertEqual(list(vec.mag),
                         [cmath.sqrt(-2),
                          cmath.sqrt(-8),
                          cmath.sqrt(-113)])

    def test_mag2(self):
        """
        Check that mag returns the square magnitude of the vectors respecting
        the metric.
        """
        vec = Vector4(4, 0, 3, 4)
        self.assertEqual(vec.mag2, -9)

        vec = Vector4(7, 2, 3, 4)
        self.assertEqual(vec.mag2, 49 - 4 - 9 - 16)

    def test_mag2_vectorized(self):
        """
        Check that mag returns the square magnitude of the numpy vectors
        respecting the metric.
        """
        x1 = np.array([1, 2, 5])
        x2 = np.array([1, 2, 5])
        x3 = np.array([1, 2, 7])
        x4 = np.array([1, 2, 8])
        vec = Vector4(x1, x2, x3, x4)

        self.assertEqual(list(vec.mag2), [-2, -8, -113]) 

    def test_eta(self):
        """
        Check that eta returns the pseudo-rapidity of a vector.
        """
        # Forward
        vector = Vector4(1, 0, 0, 1)
        self.assertEqual(vector.eta, float('inf'))
        vector = Vector4(0, 0, 0, 1)
        self.assertEqual(vector.eta, float('inf'))

        # Backward
        vector = Vector4(1, 0, 0, -1)
        self.assertEqual(vector.eta, float('-inf'))

        # Center
        vector = Vector4(1, 0, 1, 0)
        self.assertAlmostEqual(vector.eta, 0)
        vector = Vector4(1, 1, 0, 0)
        self.assertAlmostEqual(vector.eta, 0)

        # 45 deg
        vector = Vector4(1, 0, 1, 1)
        self.assertAlmostEqual(vector.eta, 0.8813735870195428)
        vector = Vector4(1, 1, 0, 1)
        self.assertAlmostEqual(vector.eta, 0.8813735870195428)
        vector = Vector4(10, 0, 1, 1)
        self.assertAlmostEqual(vector.eta, 0.8813735870195428)
        vector = Vector4(0, 0, 1, 1)
        self.assertAlmostEqual(vector.eta, 0.8813735870195428)

    def test_eta_vectorized(self):
        """
        Check that eta returns the pseudo-rapidity of a numpy vector.
        """
        x1 = np.array([1, 1, 1])
        x2 = np.array([0, 0, 0])
        x3 = np.array([0, 1, 1])
        x4 = np.array([1, 0, 1])
        vec = Vector4(x1, x2, x3, x4)

        etas = list(vec.eta)
        self.assertAlmostEqual(etas[0], float('inf'))
        self.assertAlmostEqual(etas[1], 0)
        self.assertAlmostEqual(etas[2], 0.8813735870195428)

    def test_theta(self):
        """
        Check that theta returns the azimuthal angle of the vector.
        """
        # Forward
        vector = Vector4(1, 0, 0, 1)
        self.assertEqual(vector.theta, 0)
        vector = Vector4(0, 0, 0, 1)
        self.assertEqual(vector.theta, 0)

        # Backward
        vector = Vector4(1, 0, 0, -1)
        self.assertEqual(vector.theta, cmath.pi)

        # Center
        vector = Vector4(1, 0, 1, 0)
        self.assertEqual(vector.theta, cmath.pi / 2)
        vector = Vector4(1, 1, 0, 0)
        self.assertEqual(vector.theta, cmath.pi / 2)

        # 45 deg
        vector = Vector4(1, 0, 1, 1)
        self.assertAlmostEqual(vector.theta, cmath.pi / 4)
        vector = Vector4(1, 1, 0, 1)
        self.assertAlmostEqual(vector.theta, cmath.pi / 4)
        vector = Vector4(10, 0, 1, 1)
        self.assertAlmostEqual(vector.theta, cmath.pi / 4)
        vector = Vector4(0, 0, 1, 1)
        self.assertAlmostEqual(vector.theta, cmath.pi / 4)

    def test_theta_vectorized(self):
        """
        Check that theta returns the azimuthal angle of the numpy vector.
        """
        x1 = np.array([1, 1, 1])
        x2 = np.array([0, 0, 0])
        x3 = np.array([0, 1, 1])
        x4 = np.array([1, 0, 1])
        vec = Vector4(x1, x2, x3, x4)

        self.assertEqual(list(vec.theta), [0, cmath.pi / 2, cmath.pi / 4])

    def test_phi(self):
        """
        Check that phi returns the polar angle of the vector.
        """
        vector = Vector4(1, 1, 0, 1)
        self.assertEqual(vector.phi, 0)
        vector = Vector4(1, 0, 1, 1)
        self.assertAlmostEqual(vector.phi, cmath.pi / 2)

        vector = Vector4(0, -1, 0, 1)
        self.assertAlmostEqual(vector.phi, cmath.pi)
        vector = Vector4(1, -1, 0, 1)
        self.assertAlmostEqual(vector.phi, cmath.pi)
        vector = Vector4(1, -1, 0, 10)
        self.assertAlmostEqual(vector.phi, cmath.pi)

        vector = Vector4(1, 0, -1, 1)
        self.assertAlmostEqual(vector.phi, -cmath.pi / 2)

    def test_phi_vectorized(self):
        """
        Check that phi returns the polar angle of the numpy vector.
        """
        x1 = np.array([1, 1, 1])
        x2 = np.array([1, -1, 0])
        x3 = np.array([0, 0, -1])
        x4 = np.array([1, 10, 1])
        vec = Vector4(x1, x2, x3, x4)

        phis = list(vec.phi)
        self.assertEqual(phis[0], 0)
        self.assertEqual(phis[1], cmath.pi)
        self.assertEqual(phis[2], -cmath.pi / 2)

    def test_trans(self):
        """
        Check that trans returns the length of the transverse vector.
        """
        vector = Vector4(1, 1, 0, 1)
        self.assertEqual(vector.trans, 1)
        vector = Vector4(1, 0, 1, 1)
        self.assertAlmostEqual(vector.trans, 1)

        vector = Vector4(0, -1, 0, 1)
        self.assertAlmostEqual(vector.trans, 1)
        vector = Vector4(1, -1, 0, 1)
        self.assertAlmostEqual(vector.trans, 1)
        vector = Vector4(1, -1, 0, 10)
        self.assertAlmostEqual(vector.trans, 1)

        vector = Vector4(1, 3, 4, 1)
        self.assertAlmostEqual(vector.trans, 5)

    def test_trans_vectorized(self):
        """
        Check that trans returns the length of the transverse vector.
        """
        x1 = np.array([1, 1, 1])
        x2 = np.array([1, -1, 3])
        x3 = np.array([0, 0, 4])
        x4 = np.array([1, 10, 1])
        vec = Vector4(x1, x2, x3, x4)

        self.assertEqual(list(vec.trans), [1, 1, 5])

class BoostTestCase(unittest.TestCase):
    """
    Test the implementation of Lorentz boosts.
    """

    def assertListAlmostEqual(self, list_a, list_b, *args, **kwds):
        list_a = list(list_a)
        list_b = list(list_b)
        if len(list_a) != len(list_b):
            self.assertEqual(list_a, list_b)

        for a, b in zip(list_a, list_b):
            self.assertAlmostEqual(a, b, *args, **kwds)


    def test_beta_simple(self):
        """
        Check that a simple, regular boost with beta parameter returns the
        boosted vector.
        """
        vector = Vector4(20, 40, 0, 0)
        boosted = vector.boost(1, 0, 0, beta=3./5)

        self.assertAlmostEqual(boosted[0], -5)
        self.assertAlmostEqual(boosted[1], 35)
        self.assertAlmostEqual(boosted[2], 0)
        self.assertAlmostEqual(boosted[3], 0)

    def test_beta_simple_vectorized(self):
        """
        Check that a simple, regular boost with beta parameter returns the
        boosted numpy vector.
        """
        x1 = np.array([20, 40])
        x2 = np.array([40, 80])
        x3 = np.array([0, 0])
        x4 = np.array([0, 0])
        vector = Vector4(x1, x2, x3, x4)

        boosted = vector.boost(1, 0, 0, beta=3./5)

        self.assertListAlmostEqual(boosted[0], [-5, -10])
        self.assertListAlmostEqual(boosted[1], [35, 70])
        self.assertListAlmostEqual(boosted[2], [0, 0])
        self.assertListAlmostEqual(boosted[3], [0, 0])

    def test_beta(self):
        """
        Check that a regular boost with beta parameter returns the boosted
        vector.
        """
        vector = Vector4(1, 2, 3, 4)
        boosted = vector.boost(5, 3, 4, beta=0.5)

        self.assertAlmostEqual(boosted[0], -1.7030374948677893)
        self.assertAlmostEqual(boosted[1], 2.1332035938635183)
        self.assertAlmostEqual(boosted[2], 3.0799221563181116)
        self.assertAlmostEqual(boosted[3], 4.106562875090814)

    def test_beta_vecrorized(self):
        """
        Check that a regular boost with beta parameter returns the boosted
        numpy vector.
        """
        x1 = np.array([1, -2])
        x2 = np.array([2, -4])
        x3 = np.array([3, -6])
        x4 = np.array([4, -8])
        vector = Vector4(x1, x2, x3, x4)

        boosted = vector.boost(5, 3, 4, beta=0.5)


        result = np.array([-1.7030374948677893, 2.1332035938635183,
                           3.0799221563181116, 4.106562875090814])
        result = np.array([result, -result * 2])

        self.assertListAlmostEqual(boosted[0], result.T[0])
        self.assertListAlmostEqual(boosted[1], result.T[1])
        self.assertListAlmostEqual(boosted[2], result.T[2])
        self.assertListAlmostEqual(boosted[3], result.T[3])

    def test_beta_rest(self):
        """
        Check that a regular boost with beta=0 returns the same vector.
        """
        vector = Vector4(1, 2, 3, 4)

        boosted = vector.boost(5, 3, 4, beta=0)

        self.assertAlmostEqual(boosted[0], 1)
        self.assertAlmostEqual(boosted[1], 2)
        self.assertAlmostEqual(boosted[2], 3)
        self.assertAlmostEqual(boosted[3], 4)

    def test_beta_rest_vectorized(self):
        """
        Check that a regular boost with beta=0 returns the same numpy vector.
        """
        x1 = np.array([1, -2])
        x2 = np.array([2, -4])
        x3 = np.array([3, -6])
        x4 = np.array([4, -8])
        vector = Vector4(x1, x2, x3, x4)

        boosted = vector.boost(5, 3, 4, beta=0)

        self.assertListAlmostEqual(boosted[0], [1, -2])
        self.assertListAlmostEqual(boosted[1], [2, -4])
        self.assertListAlmostEqual(boosted[2], [3, -6])
        self.assertListAlmostEqual(boosted[3], [4, -8])

    def test_gamma_simple(self):
        """
        Check that a simple, regular boost with gamma parameter returns the
        boosted vector.
        """
        vector = Vector4(20, 40, 0, 0)
        boosted = vector.boost(1, 0, 0, gamma=5./4)

        self.assertAlmostEqual(boosted[0], -5)
        self.assertAlmostEqual(boosted[1], 35)
        self.assertAlmostEqual(boosted[2], 0)
        self.assertAlmostEqual(boosted[3], 0)

    def test_gamma_simple_vectorized(self):
        """
        Check that a simple, regular boost with gamma parameter returns the
        boosted numpy vector.
        """
        x1 = np.array([20, 40])
        x2 = np.array([40, 80])
        x3 = np.array([0, 0])
        x4 = np.array([0, 0])
        vector = Vector4(x1, x2, x3, x4)

        boosted = vector.boost(1, 0, 0, gamma=5./4)

        self.assertListAlmostEqual(boosted[0], [-5, -10])
        self.assertListAlmostEqual(boosted[1], [35, 70])
        self.assertListAlmostEqual(boosted[2], [0, 0])
        self.assertListAlmostEqual(boosted[3], [0, 0])

    def test_gamma(self):
        """
        Check that a regular boost with gamma parameter returns the boosted
        vector.
        """
        vector = Vector4(1, 2, 3, 4)
        boosted = vector.boost(5, 3, 4, gamma=1/math.sqrt(0.75))

        self.assertAlmostEqual(boosted[0], -1.7030374948677893)
        self.assertAlmostEqual(boosted[1], 2.1332035938635183)
        self.assertAlmostEqual(boosted[2], 3.0799221563181116)
        self.assertAlmostEqual(boosted[3], 4.106562875090814)

    def test_gamma_vectorized(self):
        """
        Check that a regular boost with gamma parameter returns the boosted
        numpy vector.
        """
        x1 = np.array([1, -2])
        x2 = np.array([2, -4])
        x3 = np.array([3, -6])
        x4 = np.array([4, -8])
        vector = Vector4(x1, x2, x3, x4)

        boosted = vector.boost(5, 3, 4, gamma=1/math.sqrt(0.75))

        result = np.array([-1.7030374948677893, 2.1332035938635183,
                           3.0799221563181116, 4.106562875090814])
        result = np.array([result, -result * 2])

        self.assertListAlmostEqual(boosted[0], result.T[0])
        self.assertListAlmostEqual(boosted[1], result.T[1])
        self.assertListAlmostEqual(boosted[2], result.T[2])
        self.assertListAlmostEqual(boosted[3], result.T[3])


    def test_gamma_rest(self):
        """
        Check that a regular boost with gamma=0 returns the same vector.
        """
        vector = Vector4(1, 2, 3, 4)
        boosted = vector.boost(5, 3, 4, gamma=1)

        self.assertAlmostEqual(boosted[0], 1)
        self.assertAlmostEqual(boosted[1], 2)
        self.assertAlmostEqual(boosted[2], 3)
        self.assertAlmostEqual(boosted[3], 4)

    def test_gamma_rest_vectorized(self):
        """
        Check that a regular boost with gamma=0 returns the same numpy vector.
        """
        x1 = np.array([1, -2])
        x2 = np.array([2, -4])
        x3 = np.array([3, -6])
        x4 = np.array([4, -8])
        vector = Vector4(x1, x2, x3, x4)

        boosted = vector.boost(5, 3, 4, gamma=1)

        self.assertListAlmostEqual(boosted[0], [1, -2])
        self.assertListAlmostEqual(boosted[1], [2, -4])
        self.assertListAlmostEqual(boosted[2], [3, -6])
        self.assertListAlmostEqual(boosted[3], [4, -8])

    def assertBetween(self, min, actual, max):
        self.assertLess(min, actual)
        self.assertLess(actual, max)

    def test_particle(self):
        """
        Check that a boost from a moving particle returns the correct vector.
        """
        m = 125.0

        # Pair of taus in the y-z-plane
        tau_1 = Momentum4.e_m_eta_phi(m / 2, 1.777, 2, math.pi / 2)
        tau_2 = Momentum4.e_m_eta_phi(m / 2, 1.777, -2, -math.pi / 2)

        # Higgs boosted in ~x direction
        higgs = Momentum4.m_eta_phi_pt(m, 0.1, 0.1, 345.6)

        tau_1 = tau_1.boost_particle(higgs)
        tau_2 = tau_2.boost_particle(higgs)

        self.assertBetween(0, tau_1.eta, 2)
        self.assertBetween(0, tau_1.phi, math.pi/2)

        self.assertBetween(-2, tau_2.eta, 0)
        self.assertBetween(-math.pi/2, tau_2.phi, 0)

        delta_R = math.sqrt((tau_1.eta - tau_2.eta)**2
                            + (tau_1.phi - tau_2.phi)**2)

        # approximation: dR = 2 * m / pT
        self.assertAlmostEqual(delta_R, 2 * higgs.m / higgs.p_t, 1)

    def test_particle_vectorized(self):
        """
        Check that a boost from a moving particle returns the correct vector.
        """
        m = 125.0

        # Pair of taus in the y-z-plane
        x1 = np.array([m / 2, m / 2])
        x2 = np.array([1.777, 1.777])
        x3 = np.array([2, -2])
        x4 = np.array([math.pi / 2, -math.pi / 2])
        taus = Momentum4.e_m_eta_phi(x1, x2, x3, x4)

        # Higgs boosted in ~x direction
        higgs = Momentum4.m_eta_phi_pt(m, 0.1, 0.1, 345.6)

        taus = taus.boost_particle(higgs)

        self.assertBetween(0, taus.eta[0], 2)
        self.assertBetween(0, taus.phi[0], math.pi/2)

        self.assertBetween(-2, taus.eta[1], 0)
        self.assertBetween(-math.pi/2, taus.phi[1], 0)

        delta_R = math.sqrt((taus.eta[1] - taus.eta[0])**2
                            + (taus.phi[1] - taus.phi[0])**2)

        # approximation: dR = 2 * m / pT
        self.assertAlmostEqual(delta_R, 2 * higgs.m / higgs.p_t, 1)

    def test_vectorized_beta(self):
        """
        Check that a vectorized beta parameter can be used.
        """
        vector = Vector4(1, 2, 3, 4)
        boosted = vector.boost(5, 3, 4, beta=[0, 0.5])

        self.assertListAlmostEqual(boosted[0], [1, -1.7030374948677893])
        self.assertListAlmostEqual(boosted[1], [2, 2.1332035938635183])
        self.assertListAlmostEqual(boosted[2], [3, 3.0799221563181116])
        self.assertListAlmostEqual(boosted[3], [4, 4.106562875090814])

    def test_vectorized_gamma(self):
        """
        Check that a vectorized gamma parameter can be used.
        """
        vector = Vector4(1, 2, 3, 4)
        boosted = vector.boost(5, 3, 4, gamma=[1, 1/math.sqrt(0.75)])

        self.assertListAlmostEqual(boosted[0], [1, -1.7030374948677893])
        self.assertListAlmostEqual(boosted[1], [2, 2.1332035938635183])
        self.assertListAlmostEqual(boosted[2], [3, 3.0799221563181116])
        self.assertListAlmostEqual(boosted[3], [4, 4.106562875090814])

    def test_beta_vecrorized_axis(self):
        """Check that operand and beta can be vectorized."""
        vector = Vector4([1, -1], [2, -2], [3, -3], [4, -4])

        boosted = vector.boost([5, 5], [3, 3], [4, 4], beta=0.5)


        result = np.array([[-1.7030374948677893, 2.1332035938635183,
                            3.0799221563181116, 4.106562875090814],
                           [1.7030374948677893, -2.1332035938635183,
                            -3.0799221563181116, -4.106562875090814]])

        self.assertListAlmostEqual(boosted[0], result.T[0])
        self.assertListAlmostEqual(boosted[1], result.T[1])
        self.assertListAlmostEqual(boosted[2], result.T[2])
        self.assertListAlmostEqual(boosted[3], result.T[3])

    def test_beta_vecrorized_both(self):
        """Check that operand and beta can be vectorized."""
        x1 = np.array([1, -2])
        x2 = np.array([2, -4])
        x3 = np.array([3, -6])
        x4 = np.array([4, -8])
        vector = Vector4(x1, x2, x3, x4)

        boosted = vector.boost(5, 3, 4, beta=[0.5, 0])


        result = np.array([[-1.7030374948677893, 2.1332035938635183,
                            3.0799221563181116, 4.106562875090814],
                           [-2, -4, -6, -8]])

        self.assertListAlmostEqual(boosted[0], result.T[0])
        self.assertListAlmostEqual(boosted[1], result.T[1])
        self.assertListAlmostEqual(boosted[2], result.T[2])
        self.assertListAlmostEqual(boosted[3], result.T[3])

    def test_gamma_vecrorized_both(self):
        """Check that operand and gamma can be vectorized."""
        x1 = np.array([1, -2])
        x2 = np.array([2, -4])
        x3 = np.array([3, -6])
        x4 = np.array([4, -8])
        vector = Vector4(x1, x2, x3, x4)

        boosted = vector.boost(5, 3, 4, gamma=[1/math.sqrt(0.75), 1])


        result = np.array([[-1.7030374948677893, 2.1332035938635183,
                            3.0799221563181116, 4.106562875090814],
                           [-2, -4, -6, -8]])

        self.assertListAlmostEqual(boosted[0], result.T[0])
        self.assertListAlmostEqual(boosted[1], result.T[1])
        self.assertListAlmostEqual(boosted[2], result.T[2])
        self.assertListAlmostEqual(boosted[3], result.T[3])

    def test_beta_vecrorized_all(self):
        """Check that operand and beta can be vectorized."""
        vector = Vector4([1, -1], [2, -2], [3, -3], [4, -4])

        boosted = vector.boost([5, 1], [3, 3], [4, 2], beta=[0.5, 0])


        result = np.array([[-1.7030374948677893, 2.1332035938635183,
                            3.0799221563181116, 4.106562875090814],
                           [-1, -2, -3, -4]])

        self.assertListAlmostEqual(boosted[0], result.T[0])
        self.assertListAlmostEqual(boosted[1], result.T[1])
        self.assertListAlmostEqual(boosted[2], result.T[2])
        self.assertListAlmostEqual(boosted[3], result.T[3])


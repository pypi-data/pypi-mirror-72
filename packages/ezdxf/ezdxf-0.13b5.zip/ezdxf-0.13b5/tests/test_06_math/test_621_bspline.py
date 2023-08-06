# Created: 06.01.2012
# Copyright (c) 2012-2018 Manfred Moitzi
# License: MIT License
import pytest
from math import isclose
from ezdxf.math.bspline import BSpline, DBSpline
from ezdxf.math.bspline import bspline_basis_vector, Basis, open_uniform_knot_vector, normalize_knots, subdivide_params

DEFPOINTS = [(0.0, 0.0, 0.0), (10., 20., 20.), (30., 10., 25.), (40., 10., 25.), (50., 0., 30.)]


def test_bspine_points():
    curve = BSpline(DEFPOINTS, order=3)
    points = list(curve.approximate(40))

    for rpoint, epoint in zip(points, iter_points(DBSPLINE, 0)):
        epx, epy, epz = epoint
        rpx, rpy, rpz = rpoint
        assert isclose(epx, rpx)
        assert isclose(epy, rpy)
        assert isclose(epz, rpz)


def test_bspline_basis_vector():
    degree = 3
    count = 10
    knots = list(open_uniform_knot_vector(count, order=degree + 1))
    max_t = max(knots)
    basis_func = Basis(knots=knots, order=degree + 1, count=count)
    for u in (0, 2., 2.5, 3.5, 4., max_t):
        basis = bspline_basis_vector(u, count=count, degree=degree, knots=knots)
        basis2 = basis_func.basis(u)
        assert len(basis) == len(basis2)
        assert basis == basis2


@pytest.fixture()
def dbspline():
    curve = DBSpline(DEFPOINTS, order=3)
    return list(curve.approximate(40))


def iter_points(values, n):
    return (data[n] for data in values)


def iter_data(result, n):
    return zip(iter_points(result, n), iter_points(DBSPLINE, n))


def test_dbspline_points(dbspline):
    for rpoint, epoint in iter_data(dbspline, 0):
        epx, epy, epz = epoint
        rpx, rpy, rpz = rpoint
        assert isclose(epx, rpx)
        assert isclose(epy, rpy)
        assert isclose(epz, rpz)


def test_normalize_knots():
    assert normalize_knots([0, 0.25, 0.5, 0.75, 1.0]) == [0, 0.25, 0.5, 0.75, 1.0]
    assert normalize_knots([0, 1, 2, 3, 4]) == [0, 0.25, 0.5, 0.75, 1.0]
    assert normalize_knots([2, 3, 4, 5, 6]) == [0, 0.25, 0.5, 0.75, 1.0]


def test_normalize_knots_if_needed():
    s = BSpline(
        control_points=DEFPOINTS,
        knots=[2, 2, 2, 2, 3, 6, 6, 6, 6],
        order=4,
    )
    k = s.knots()
    assert k[0] == 0.0


def test_dbspline_derivative_1(dbspline):
    for rpoint, epoint in iter_data(dbspline, 1):
        epx, epy, epz = epoint
        rpx, rpy, rpz = rpoint
        assert isclose(epx, rpx)
        assert isclose(epy, rpy)
        assert isclose(epz, rpz)


def test_dbspline_derivative_2(dbspline):
    for rpoint, epoint in iter_data(dbspline, 2):
        epx, epy, epz = epoint
        rpx, rpy, rpz = rpoint
        assert isclose(epx, rpx)
        assert isclose(epy, rpy)
        assert isclose(epz, rpz)


def test_bspline_insert_knot():
    bspline = BSpline([(0, 0), (10, 20), (30, 10), (40, 10), (50, 0), (60, 20), (70, 50), (80, 70)])
    t = bspline.max_t / 2
    assert len(bspline.control_points) == 8
    bspline.insert_knot(t)
    assert len(bspline.control_points) == 9


def test_transform_interface():
    from ezdxf.math import Matrix44
    spline = BSpline(control_points=[(1, 0, 0), (3, 3, 0), (6, 0, 1)], order=3)
    spline.transform(Matrix44.translate(1, 2, 3))
    assert spline.control_points[0] == (2, 2, 3)


def test_bezier_decomposition():
    bspline = BSpline.from_fit_points([(0, 0), (10, 20), (30, 10), (40, 10), (50, 0), (60, 20), (70, 50), (80, 70)])
    bezier_segments = list(bspline.bezier_decomposition())
    assert len(bezier_segments) == 5
    # results visually checked to be correct
    assert bezier_segments[0] == [
        (0.0, 0.0, 0.0),
        (2.02070813064438, 39.58989657555839, 0.0),
        (14.645958536022286, 10.410103424441612, 0.0),
        (30.0, 10.0, 0.0)
    ]
    assert bezier_segments[-1] == [
        (60.0, 20.0, 0.0),
        (66.33216513897267, 43.20202388489432, 0.0),
        (69.54617236126121, 50.37880459351478, 0.0),
        (80.0, 70.0, 0.0)
    ]


def test_cubic_bezier_approximation():
    bspline = BSpline.from_fit_points([(0, 0), (10, 20), (30, 10), (40, 10), (50, 0), (60, 20), (70, 50), (80, 70)])
    bezier_segments = list(bspline.cubic_bezier_approximation(level=3))
    assert len(bezier_segments) == 28
    bezier_segments = list(bspline.cubic_bezier_approximation(segments=40))
    assert len(bezier_segments) == 40
    # The interpolation is based on cubic_bezier_interpolation()
    # and therefore the interpolation result is not topic of this test.


def test_subdivide_params():
    assert list(subdivide_params([0.0, 1.0])) == [0.0, 0.5, 1.0]
    assert list(subdivide_params([0.0, 0.5, 1.0])) == [0.0, 0.25, 0.5, 0.75, 1.0]


DBSPLINE = [
    [[0.0, 0.0, 0.0], [20.0, 40.0, 40.0], [0.0, -50.0, -35.0]],
    [[1.5000000000000002, 2.8593750000000004, 2.9015625000000003], [20.0, 36.25, 37.375], [0.0, -50.0, -35.0]],
    [[2.9999999999999996, 5.437499999999999, 5.606249999999999], [20.0, 32.5, 34.75], [0.0, -50.0, -35.0]],
    [[4.499999999999999, 7.734374999999999, 8.1140625], [20.0, 28.750000000000004, 32.125], [0.0, -50.0, -35.0]],
    [[5.999999999999999, 9.749999999999998, 10.424999999999999], [20.0, 24.999999999999996, 29.499999999999996],
     [0.0, -50.0, -35.0]],
    [[7.5, 11.484375, 12.5390625], [20.0, 21.25, 26.875], [0.0, -50.0, -35.0]],
    [[8.999999999999998, 12.937499999999998, 14.456249999999999], [20.0, 17.500000000000004, 24.25],
     [0.0, -50.0, -35.0]],
    [[10.5, 14.109375000000002, 16.176562500000003], [20.0, 13.75, 21.625], [0.0, -50.0, -35.0]],
    [[12.0, 15.0, 17.7], [20.0, 10.0, 19.0], [0.0, -50.0, -35.0]],
    [[13.5, 15.609375, 19.026562499999997], [20.0, 6.250000000000005, 16.375000000000007], [0.0, -50.0, -35.0]],
    [[15.0, 15.9375, 20.15625], [20.0, 2.5, 13.75], [0.0, -50.0, -35.0]],
    [[16.5, 15.984375, 21.089062499999997], [20.0, -1.25, 11.125], [0.0, -50.0, -35.0]],
    [[17.999999999999996, 15.75, 21.825], [20.0, -4.999999999999995, 8.500000000000002], [0.0, -50.0, -35.0]],
    [[19.5, 15.234375, 22.3640625], [20.0, -8.75, 5.875], [0.0, -50.0, -35.0]],
    [[20.9875, 14.5125, 22.74375], [19.5, -9.5, 4.749999999999997], [-10.0, 10.0, -5.0]],
    [[22.421875, 13.828125, 23.0859375], [18.75, -8.75, 4.375], [-10.0, 10.0, -5.0]],
    [[23.799999999999997, 13.2, 23.4], [18.0, -8.0, 4.000000000000001], [-10.0, 10.0, -5.0]],
    [[25.121875, 12.628124999999999, 23.6859375], [17.25, -7.250000000000001, 3.625], [-10.0, 10.0, -5.0]],
    [[26.3875, 12.112499999999999, 23.943749999999998], [16.5, -6.500000000000002, 3.25], [-10.0, 10.0, -5.0]],
    [[27.596875, 11.653125, 24.1734375], [15.749999999999996, -5.75, 2.875], [-10.0, 10.0, -5.0]],
    [[28.75, 11.25, 24.375], [15.0, -5.0, 2.5], [-10.0, 10.0, -5.0]],
    [[29.846874999999997, 10.903125, 24.5484375], [14.250000000000004, -4.25, 2.125], [-10.0, 10.0, -5.0]],
    [[30.887500000000003, 10.6125, 24.69375], [13.5, -3.500000000000001, 1.75], [-10.0, 10.0, -5.0]],
    [[31.871875, 10.378125, 24.8109375], [12.749999999999996, -2.7500000000000018, 1.3749999999999964],
     [-10.0, 10.0, -5.0]],
    [[32.8, 10.2, 24.900000000000002], [12.0, -2.0000000000000018, 1.0000000000000036], [-10.0, 10.0, -5.0]],
    [[33.671875, 10.078125, 24.9609375], [11.25, -1.25, 0.625], [-10.0, 10.0, -5.0]],
    [[34.4875, 10.0125, 24.99375], [10.500000000000007, -0.5, 0.25000000000000355], [-10.0, 10.0, -5.0]],
    [[35.253125, 9.993749999999999, 25.003125], [10.250000000000002, -0.49999999999999645, 0.24999999999999822],
     [10.0, -20.0, 10.0]],
    [[36.05, 9.899999999999999, 25.05], [11.000000000000002, -2.0000000000000027, 1.0000000000000018],
     [10.0, -20.0, 10.0]],
    [[36.903125, 9.693750000000001, 25.153125000000003], [11.749999999999996, -3.4999999999999964, 1.75],
     [10.0, -20.0, 10.0]],
    [[37.8125, 9.375, 25.3125], [12.5, -5.0, 2.5], [10.0, -20.0, 10.0]],
    [[38.778124999999996, 8.943750000000001, 25.528125], [13.249999999999996, -6.499999999999995, 3.25],
     [10.0, -20.0, 10.0]],
    [[39.8, 8.4, 25.799999999999997], [14.0, -7.999999999999998, 4.0], [10.0, -20.0, 10.0]],
    [[40.878125, 7.743749999999999, 26.128124999999997], [14.75, -9.500000000000002, 4.75], [10.0, -20.0, 10.0]],
    [[42.0125, 6.975000000000003, 26.512500000000003], [15.5, -10.999999999999996, 5.4999999999999964],
     [10.0, -20.0, 10.0]],
    [[43.203125, 6.09375, 26.953125], [16.25, -12.5, 6.25], [10.0, -20.0, 10.0]],
    [[44.44999999999999, 5.100000000000004, 27.449999999999996], [16.999999999999993, -13.999999999999996, 7.0],
     [10.0, -20.0, 10.0]],
    [[45.753125, 3.9937500000000017, 28.003125], [17.75, -15.499999999999996, 7.75], [10.0, -20.0, 10.0]],
    [[47.112500000000004, 2.7749999999999986, 28.6125], [18.5, -17.000000000000004, 8.5], [10.0, -20.0, 10.0]],
    [[48.52812499999999, 1.4437500000000032, 29.278124999999996],
     [19.250000000000014, -18.499999999999993, 9.249999999999993], [10.0, -20.0, 10.0]],
    [[50.0, 0.0, 30.0], [20.0, -20.0, 10.0], [10.0, -20.0, 10.0]]
]

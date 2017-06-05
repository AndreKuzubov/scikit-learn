from scipy.integrate import *
from sympy import *
from numpy import *


# public
def countingH(point):
    k = array([point[0], 0, point[1], 0])
    h = getRating(k)
    return h


# public
def countingHs(points):
    Xs = points[:len(points) / 2]
    Ys = points[len(points) / 2:len(points)]
    hs = []
    for i in xrange(len(Xs)):
        hs = hs + [countingH([Xs[i], Ys[i]])]
    return hs


# private
def getRating(params):
    t = arange(0, 20, 0.01)
    state0 = [3.14, 0, 0, 0]
    state = odeint(pendulumOnCarriage, state0, t, args=(params,))
    return rating(state)


# private
def pendulumOnCarriage(state, t, k):
    a = state[0]
    da = state[1]
    x = state[2]
    dx = state[3]

    M = 1
    m = 0.3
    l = 1
    g = 9.8
    f = 0

    # controller
    x = array([a, da, x, dx])
    f = dot(x, k)

    D = l * M + l * m * (sin(a)) ** 2
    dda = ((M + m) * g * sin(a) - m * l * (da ** 2) * sin(a) * cos(a) - f * cos(a)) / D
    ddx = (m * (l ** 2) * (da ** 2) * sin(a) + l * f - m * g * l * sin(a) * cos(a)) / D
    return [da, dda, dx, ddx]


# private
def rating(state):
    sa = 0
    sx = 0
    sDx = 0
    for i in xrange(len(state)):
        a = state[i][0]
        da = state[i][1]
        x = state[i][2]
        dx = state[i][3]
        # align alpha
        d = a / 6.28
        d = round(d)
        a = abs(a - d * 6.28)
        # counting sum deviation alpha
        deviationA = abs(3.14 - a)
        # print 'stateA = ',state[i][0], 'a = ',a,'deviation a= ',deviationA
        # (exp(deviationA)-1)*3.14/22.1039 - prioritization deviation alpha
        sa = sa + (exp(deviationA) - 1) * 3.14 / 22.1039
        # sum x,dx,da
        sx = sx + abs(x)
        sDx = sDx + abs(dx)

    sa = sa / len(state)

    # better more deviation
    pa = abs(sa) / 3.15

    # max x deviation = 10
    sx = sx / len(state)
    # if (sx > 10): sx=10
    px = abs((1 - sx / 10))

    # max sDx deviation = 4
    sDx = sDx / len(state)
    # if (sDx >4): sDx=4
    pDx = abs((1 - sDx / 4))

    p = (pa * 58 / 60 + px / 60 + pDx / 60)

    # best = 1, bad =0
    rating = exp(-p)

    return rating

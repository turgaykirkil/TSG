//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 16.08.2020.
//

import Foundation

public class Distribution{
    
    private static let Z_MAX = 6.0
    private static let Z_EPSILON = 0.000001
    private static let CHI_EPSILON = 0.000001
    private static let CHI_MAX = 99999.0
    private static let LOG_SQRT_PI = 0.5723649429247000870717135
    private static let I_SQRT_PI = 0.5641895835477562869480795
    private static let BIGX = 200.0
    private static let I_PI = 0.3183098861837906715377675
    private static let F_EPSILON = 0.000001
    private static let F_MAX = 9999.0

    /**
    The ex method takes a double x as an input, if x is less than -BIGX it returns 0, otherwise it returns Euler's
    number e raised to the power of x.

    - Parameter x : double input.

    - Returns: 0 if input is less than -BIGX, Euler's number e raised to the power of x otherwise.
    */
    static public func __ex(x: Double) -> Double{
        if x < -Distribution.BIGX{
            return 0
        }
        return exp(x)
    }

    /**
    The beta method takes a double list x as an input. It loops through x and accumulates
    the value of gammaLn(x), also it sums up the items of x and returns (accumulated result - gammaLn of this
    summation).

    - Parameter x : double list input.

    - Returns: beta distribution at poInt x.
    */
    static public func beta(x: [Double]) -> Double{
        var total : Double = 0.0
        var result : Double = 0.0
        for i in 0..<x.count{
            result += Distribution.gammaLn(x: x[i])
            total += x[i]
        }
        result -= Distribution.gammaLn(x: total)
        return result
    }

    /**
    The gammaLn method takes a double x as an input and returns the logarithmic result of the gamma distribution at
    poInt x.

    - Parameter x : double input.

    - Returns: the logarithmic result of the gamma distribution at poInt x.
    */
    static public func gammaLn(x: Double) -> Double{
        let cof = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5]
        var y : Double = x
        var tmp : Double = x + 5.5
        tmp -= (x + 0.5) * log(tmp)
        var ser : Double = 1.000000000190015
        for j in 0..<6{
            y = y + 1
            ser += cof[j] / y
        }
        return -tmp + log(2.5066282746310005 * ser / x)
    }

    /**
    The zNormal method performs the Z-Normalization. It ensures, that all elements of the input vector are
    transformed Into the output vector whose mean is approximately 0 while the standard deviation is in a range
    close to 1.

    - Parameter z : double input.

    - Returns: normalized value of given input.
    */
    static public func zNormal(z: Double) -> Double{
        var y, x, w : Double
        if z == 0.0{
            x = 0.0
        } else{
            y = 0.5 * abs(z)
            if y >= Distribution.Z_MAX * 0.5{
                x = 1.0
            } else {
                if y < 1.0{
                    w = y * y
                    x = ((((((((0.000124818987 * w - 0.001075204047) * w + 0.005198775019) * w - 0.019198292004) * w
                             + 0.059054035642) * w - 0.151968751364) * w + 0.319152932694) * w - 0.531923007300) * w
                         + 0.797884560593) * y * 2.0
                }  else {
                    y -= 2.0
                    x = (((((((((((((-0.000045255659 * y + 0.000152529290) * y - 0.000019538132) * y
                                   - 0.000676904986) * y + 0.001390604284) * y - 0.000794620820) * y
                                - 0.002034254874) * y + 0.006549791214) * y - 0.010557625006) * y + 0.011630447319) * y
                            - 0.009279453341) * y + 0.005353579108) * y - 0.002141268741) * y + 0.000535310849) * y + 0.999936657524
                }
            }
        }
        if z > 0.0{
            return (x + 1.0) * 0.5
        } else {
            return (1.0 - x) * 0.5
        }
    }

    /**
    The zInverse method returns the Z-Inverse of given probability value.

    - Parameter p : probability input.

    - Returns: the Z-Inverse of given probability.
    */
    static public func zInverse(p: Double) -> Double{
        var minz : Double = -Distribution.Z_MAX
        var maxz : Double = Distribution.Z_MAX
        var zval : Double = 0.0
        if p <= 0.0 || p >= 1.0{
            return 0.0
        }
        while maxz - minz > Distribution.Z_EPSILON{
            let pval : Double = Distribution.zNormal(z: zval)
            if pval > p{
                maxz = zval
            } else {
                minz = zval
            }
            zval = (maxz + minz) * 0.5
        }
        return zval
    }

    /**
    The chiSquare method is used to determine whether there is a significant difference between the expected
    frequencies and the observed frequencies in one or more categories. It takes a double input x and an Integer
    freedom for degrees of freedom as inputs. It returns the Chi Squared result.

    - Parameters:
        - x : double input.
        - freedom : -Integer input for degrees of freedom.

    - Returns: the Chi Squared result.
     */
    static public func chiSquare(x: Double, freedom: Int) -> Double{
        var a, s, e, c, z : Double
        var y : Double = 0
        var even : Bool
        if x <= 0.0 || freedom < 1{
            return 1.0
        }
        a = 0.5 * x
        even = (freedom % 2 == 0)
        if freedom > 1{
            y = Distribution.__ex(x: -a)
        }
        if even{
            s = y
        } else {
            s = 2.0 * Distribution.zNormal(z: -sqrt(x))
        }
        if freedom > 2{
            let newX : Double = 0.5 * (Double(freedom) - 1.0)
            if even{
                z = 1.0
            } else {
                z = 0.5
            }
            if a > Distribution.BIGX {
                if even {
                    e = 0.0
                } else {
                    e = Distribution.LOG_SQRT_PI
                }
                c = log(a)
                while z <= newX {
                    e = log(z) + e
                    s += Distribution.__ex(x: c * z - a - e)
                    z += 1.0
                }
                return s
            } else {
                if even {
                    e = 1.0
                } else {
                    e = Distribution.I_SQRT_PI / sqrt(a)
                }
                c = 0.0
                while z <= newX {
                    e = e * (a / z)
                    c = c + e
                    z += 1.0
                }
                return c * y + s
            }
        } else {
            return s
        }
    }

    /**
    The chiSquareInverse method returns the Chi Square-Inverse of given probability value with given degree of
    freedom.

    - Parameters:
        - p : probability input.
        - freedom : Integer input for degrees of freedom.

    - Returns: the chiSquare-Inverse of given probability.
    */
    static public func chiSquareInverse(p: Double, freedom: Int) -> Double{
        var minchisq : Double = 0.0
        var maxchisq : Double = Distribution.CHI_MAX
        if p <= 0.0{
            return maxchisq
        } else {
            if p >= 1.0 {
                return 0.0
            }
        }
        var chisqval : Double = Double(freedom) / sqrt(p)
        while maxchisq - minchisq > Distribution.CHI_EPSILON{
            if Distribution.chiSquare(x: chisqval, freedom: freedom) < p{
                maxchisq = chisqval
            } else {
                minchisq = chisqval
            }
            chisqval = (maxchisq + minchisq) * 0.5
        }
        return chisqval
    }

    /**
    The fDistribution method is used to observe whether two samples have the same variance. It takes a double input
    F and two Integer freedom1 and freedom2 for degrees of freedom as inputs. It returns the F-Distribution result.

    - Parameters:
        - F : double input.
        - freedom1 : Integer input for degrees of freedom.
        - freedom2 : Integer input for degrees of freedom.

    -  Returns: the F-Distribution result.
    */
    static public func fDistribution(F: Double, freedom1: Int, freedom2: Int) -> Double{
        var i, j, a, b : Int
        var w, y, z, d, p: Double
        if F < Distribution.F_EPSILON || freedom1 < 1 || freedom2 < 1{
            return 1.0
        }
        if freedom1 % 2 != 0{
            a = 1
        } else {
            a = 2
        }
        if freedom2 % 2 != 0{
            b = 1
        } else {
            b = 2
        }
        w = F * Double(freedom1) / Double(freedom2)
        z = 1.0 / (1.0 + w)
        if a == 1 {
            if b == 1 {
                p = sqrt(w)
                y = Distribution.I_PI
                d = y * z / p
                p = 2.0 * y * atan(p)
            } else {
                p = sqrt(w * z)
                d = 0.5 * p * z / w
            }
        } else {
            if b == 1 {
                p = sqrt(z)
                d = 0.5 * z * p
                p = 1.0 - p
            } else {
                d = z * z
                p = w * z
            }
        }
        y = 2.0 * w / z
        j = b + 2
        while j <= freedom2{
            d *= (1.0 + Double(a) / (Double(j) - 2.0)) * z
            if a == 1{
                p = p + d * y / (Double(j) - 1.0)
            } else {
                p = (p + w) * z
            }
            j += 2
        }
        y = w * z
        z = 2.0 / z
        b = freedom2 - 2
        i = a + 2
        while i <= freedom1{
            j = i + b
            d *= y * Double(j) / (Double(i) - 2.0)
            p -= z * d / Double(j)
            i += 2
        }
        if p < 0.0{
            p = 0.0
        } else {
            if p > 1.0 {
                p = 1.0
            }
        }
        return 1.0 - p
    }

    /**
    The fDistributionInverse method returns the F-Distribution Inverse of given probability value.

    - Parameters :
        - p : double probability.
        - freedom1 : Integer input for degrees of freedom.
        - freedom2 : Integer input for degrees of freedom.

    - Returns: the F-Distribution Inverse of given probability.
    */
    static public func fDistributionInverse(p: Double, freedom1: Int, freedom2: Int) -> Double{
        var fval : Double
        var maxf : Double = Distribution.F_MAX
        var minf : Double = 0.0
        if p <= 0.0 || p >= 1.0{
            return 0.0
        }
        if freedom1 == freedom2 && freedom1 > 2500{
            return 1 + 4.0 / Double(freedom1)
        }
        fval = 1.0 / p
        while abs(maxf - minf) > Distribution.F_EPSILON{
            if Distribution.fDistribution(F: fval, freedom1: freedom1, freedom2: freedom2) < p{
                maxf = fval
            } else {
                minf = fval
            }
            fval = (maxf + minf) * 0.5
        }
        return fval
    }

    /**
    The tDistribution method is used instead of the normal distribution when there is small samples. It takes a
    double input T and an Integer freedom for degree of freedom as inputs. It returns the T-Distribution result by
    using F-Distribution method.

    - Parameters:
        - T : double input.
        - freedom : Integer input for degrees of freedom.

    - Returns: the T-Distribution result.
    */
    static public func tDistribution(T: Double, freedom: Int) -> Double{
        if T >= 0 {
            return Distribution.fDistribution(F: T * T, freedom1: 1, freedom2: freedom) / 2
        } else {
            return 1 - Distribution.fDistribution(F: T * T, freedom1: 1, freedom2: freedom) / 2
        }
    }

    /**
    The tDistributionInverse method returns the T-Distribution Inverse of given probability value.

    - Parameters:
        - p : double probability.
        - freedom : Integer input for degrees of freedom.

    - Returns: the T-Distribution Inverse of given probability.
    */
    static public func tDistributionInverse(p: Double, freedom: Int) -> Double{
        if p < 0.5{
            return sqrt(Distribution.fDistributionInverse(p: p * 2, freedom1: 1, freedom2: freedom))
        } else {
            return -sqrt(Distribution.fDistributionInverse(p: (1 - p) * 2, freedom1: 1, freedom2: freedom))
        }
    }

}

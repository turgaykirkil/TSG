//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 16.08.2020.
//

import Foundation


public class Matrix : NSCopying{
    
    private var __row: Int
    private var __col: Int
    private var __values: [[Double]]
    
    /**
     * Another constructor of {@link Matrix} class which takes row and column numbers as inputs and creates new values
     * {@link java.lang.reflect.Array} with given parameters.
     *
     * - Parameters:
     *      - row: is used to create matrix.
     *      - col: is used to create matrix.
     */
    public init(row: Int, col: Int){
        self.__row = row
        self.__col = col
        self.__values = Array(repeating: Array(repeating: 0.0, count: col), count: row)
    }

    /// The overridden clone method creates new Matrix and copies the content of values array into new matrix.
    /// - Parameter zone: -
    /// - Returns: Matrix which is the copy of values array.
    public func copy(with zone: NSZone? = nil) -> Any {
        let copy = Matrix(row: __row, col: __col)
        for i in 0..<self.__row{
            for j in 0..<self.__col{
                copy.__values[i][j] = __values[i][j]
            }
        }
        return copy
    }

    /**
     * Another constructor of {@link Matrix} class which takes row, column, minimum and maximum values as inputs.
     * First it creates new values {@link java.lang.reflect.Array} with given row and column numbers. Then fills in the
     * positions with random numbers using minimum and maximum inputs.
     *
     * - Parameters:
     *      - row: is used to create matrix.
     *      - col: is used to create matrix.
     *      - min: minimum value.
     *      - max: maximum value.
     */
    public init(row: Int, col: Int, min: Double, max: Double, random: Random){
        self.__row = row
        self.__col = col
        self.__values = Array(repeating: Array(repeating: 0.0, count: col), count: row)
        for i in 0..<row{
            for j in 0..<col{
                self.__values[i][j] = random.nextDouble(min: min, max: max)
            }
        }
    }
    
    /**
     * Another constructor of {@link Matrix} class which takes size as input and creates new values {@link java.lang.reflect.Array}
     * with using size input and assigns 1 to each element at the diagonal.
     *
     * - Parameter size: is used declaring the size of the array.
     */
    public init(size: Int){
        self.__row = size
        self.__col = size
        self.__values = Array(repeating: Array(repeating: 0.0, count: size), count: size)
        for i in 0..<size{
            self.__values[i][i] = 1.0
        }
    }
    
    /// Initializes the matrix y multiplying two vectors of sizes n times 1 and 1 times m.
    /// - Parameters:
    ///   - rowVector: Row vector of size n times 1
    ///   - colVector: Column vector of size 1 times m
    public init(rowVector: Vector, colVector: Vector){
        self.__row = rowVector.size()
        self.__col = colVector.size()
        self.__values = Array(repeating: Array(repeating: 0.0, count: colVector.size()), count: rowVector.size())
        for i in 0..<rowVector.size(){
            for j in 0..<colVector.size(){
                self.__values[i][j] = rowVector.getValue(index: i) * colVector.getValue(index: j)
            }
        }
    }
    
    /**
    The getter for the index at given rowNo and colNo of values list.

    - Parameters:
        - rowNo : integer input for row number.
        - colNo : integer input for column number.

    - Returns: item at given index of values list.
    */
    public func getValue(rowNo: Int, colNo: Int) -> Double{
        return self.__values[rowNo][colNo]
    }

    /**
    The setter for the value at given index of values list.

    - Parameters:
        - rowNo : integer input for row number.
        - colNo : integer input for column number.
        - value : is used to set at given index.
    */
    public func setValue(rowNo: Int, colNo: Int, value: Double){
        self.__values[rowNo][colNo] = value
    }

    /**
    The addValue method adds the given value to the item at given index of values list.

    - Parameters:
        - rowNo : integer input for row number.
        - colNo : integer input for column number.
        - value : is used to add to given item at given index.
    */
    public func addValue(rowNo: Int, colNo: Int, value: Double){
        self.__values[rowNo][colNo] += value
    }

    /**
    The increment method adds 1 to the item at given index of values list.

    - Parameters:
        - rowNo : integer input for row number.
        - colNo : integer input for column number.
    */
    public func increment(rowNo: Int, colNo: Int){
        self.__values[rowNo][colNo] += 1
    }

    /**
    The getter for the row variable.

    - Returns: row number.
    */
    public func getRow() -> Int{
        return self.__row
    }

    /**
    The getRowVector method returns the vector of values list at given row input.

    - Parameter row : row integer input for row number.

    - Returns: Vector of values list at given row input.
    */
    public func getRowVector(row: Int) -> Vector{
        let rowList : [Double] = self.__values[row]
        let rowVector : Vector = Vector(values: rowList)
        return rowVector
    }

    /**
    The getter for the col variable.

    - Returns: column number.
    */
    public func getColumn() -> Int{
        return self.__col
    }

    /**
     * The getColumnVector method creates a Vector and adds items at given column number of values list
     * to the Vector.
     - Parameter column : column integer input for column number.
     *
     - Returns: Vector of given column number.
    */
    public func getColumnVector(column: Int) -> [Double]{
        var columnVector : [Double] = []
        for i in 0..<self.__row{
            columnVector.append(self.__values[i][column])
        }
        return columnVector
    }

    /**
    The columnWiseNormalize method, first accumulates items column by column then divides items
    by the summation.
    */
    public func columnWiseNormalize(){
        for i in 0..<self.__row{
            var total : Double = 0
            for j in 0..<self.__col{
                total += self.__values[i][j]
            }
            for j in 0..<self.__col{
                self.__values[i][j] = self.__values[i][j] / total
            }
        }
    }

    /**
    The multiplyWithConstant method takes a constant as an input and multiplies each item of values list
    with given constant.

    - Parameter constant : constant value to multiply items of values list.
    */
    public func multiplyWithConstant(constant: Double){
        for i in 0..<self.__row{
            for j in 0..<self.__col{
                self.__values[i][j] *= constant
            }
        }
    }

    /**
    The divideByConstant method takes a constant as an input and divides each item of values list
    with given constant.

    - Parameter constant : constant value to divide items of values list.
    */
    public func divideByConstant(constant: Double){
        for i in 0..<self.__row{
            for j in 0..<self.__col{
                self.__values[i][j] /= constant
            }
        }
    }

    /**
    The add method takes a Matrix as an input and accumulates values list with the
    corresponding items of given Matrix. If the sizes of both Matrix and values list do not match,
    it throws MatrixDimensionMismatch exception.

    - Parameter m : Matrix type input.
    */
    public func add(m: Matrix){
        for i in 0..<self.__row{
            for j in 0..<self.__col{
                self.__values[i][j] += m.__values[i][j]
            }
        }
    }

    /**
    The add method which takes a row number and a Vector as inputs. It sums up the corresponding values at the given
    row of values list and given Vector. If the sizes of both Matrix and values list do not match, it throws
    MatrixColumnMismatch exception.

    - Parameters
    ----------
    rowNo : Int
        integer input for row number.
    v : Vector
        Vector type input.
    */
    public func addRowVector(rowNo: Int, v: Vector){
        for i in 0..<self.__col{
            self.__values[rowNo][i] += v.getValue(index: i)
        }
    }

    /**
    The subtract method takes a Matrix as an input and subtracts from values list the
    corresponding items of given Matrix. If the sizes of both Matrix and values list do not match,
    it throws {@link MatrixDimensionMismatch} exception.

    - Parameter m : Matrix type input.
    */
    public func subtract(m: Matrix){
        for i in 0..<self.__row{
            for j in 0..<self.__col{
                self.__values[i][j] -= m.__values[i][j]
            }
        }
    }

    /**
    The multiplyWithVectorFromLeft method takes a Vector as an input and creates a result list.
    Then, multiplies values of input Vector starting from the left side with the values list,
    accumulates the multiplication, and assigns to the result list. If the sizes of both Vector
    and row number do not match, it throws MatrixRowMismatch exception.

    - Parameter v : Vector type input.

    - Returns: Vector that holds the result.
    */
    public func multiplyWithVectorFromLeft(v: Vector) -> Vector{
        let result : Vector = Vector(size: 0, x: 0)
        for i in 0..<self.__col{
            var total : Double = 0.0
            for j in 0..<self.__row{
                total += v.getValue(index: j) * self.__values[j][i]
            }
            result.add(x: total)
        }
        return result
    }

    /**
    The multiplyWithVectorFromRight method takes a Vector as an input and creates a result list.
    Then, multiplies values of input Vector starting from the right side with the values list,
    accumulates the multiplication, and assigns to the result list. If the sizes of both Vector
    and row number do not match, it throws MatrixColumnMismatch exception.

    - Parameter v : Vector type input.

    - Returns: Vector that holds the result.
    */
    public func multiplyWithVectorFromRight(v: Vector) -> Vector{
        let result : Vector = Vector(size: 0, x: 0)
        for i in 0..<self.__row{
            var total : Double = 0.0
            for j in 0..<self.__col{
                total += v.getValue(index: j) * self.__values[i][j]
            }
            result.add(x: total)
        }
        return result
    }

    /**
    The columnSum method takes a column number as an input and accumulates items at given column number of values
    list.

    - Parameter columnNo : Column number input.

    - Returns: summation of given column of values list.
    */
    public func columnSum(columnNo: Int) -> Double{
        var total : Double = 0
        for i in 0..<self.__row{
            total += self.__values[i][columnNo]
        }
        return total
    }

    /**
    The sumOfRows method creates a mew result Vector and adds the result of columnDum method's corresponding
    index to the newly created result Vector.

    - Returns: Vector that holds column sum.
    */
    public func sumOfRows() -> Vector{
        let result : Vector = Vector(size: 0, x: 0)
        for i in 0..<self.__col{
            result.add(x: self.columnSum(columnNo: i))
        }
        return result
    }

    /**
    The rowSum method takes a row number as an input and accumulates items at given row number of values list.

     - Parameter rowNo: Row number input.
     
     - Returns: summation of given row of values {@link java.lang.reflect.Array}.
    */
    public func rowSum(rowNo: Int) -> Double{
        var total : Double = 0
        for i in 0..<self.__col{
            total += self.__values[rowNo][i]
        }
        return total
    }

    /**
    The multiply method takes a Matrix as an input. First it creates a result Matrix and puts the
    accumulatated multiplication of values list and given Matrix into result
    Matrix. If the size of Matrix's row size and values list's column size do not match,
    it throws MatrixRowColumnMismatch exception.

    - Parameter m : Matrix type input.

    - Returns: result Matrix.
    */
    public func multiply(m: Matrix) -> Matrix{
        let result : Matrix = Matrix(row: self.__row, col: m.__col)
        for i in 0..<self.__row{
            for j in 0..<m.__col{
                var total : Double = 0.0
                for k in 0..<self.__col{
                    total += self.__values[i][k] * m.__values[k][j]
                }
                result.__values[i][j] = total
            }
        }
        return result
    }

    /**
    The elementProduct method takes a Matrix as an input and performs element wise multiplication. Puts result
    to the newly created Matrix. If the size of Matrix's row and column size does not match with the values
    list's row and column size, it throws MatrixDimensionMismatch exception.

    - Parameter m : Matrix type input.

    - Returns: result Matrix.
    */
    public func elementProduct(m: Matrix) -> Matrix{
        let result : Matrix = Matrix(row: self.__row, col: self.__col)
        for i in 0..<self.__row{
            for j in 0..<self.__col{
                result.__values[i][j] = self.__values[i][j] * m.__values[i][j]
            }
        }
        return result
    }

    /**
    The sumOfElements method accumulates all the items in values list and
    returns this summation.

    - Returns: sum of the items of values list.
    */
    public func sumOfElements() -> Double{
        var total : Double = 0.0
        for i in 0..<self.__row{
            total += rowSum(rowNo: i)
        }
        return total
    }

    /**
    The trace method accumulates items of values list at the diagonal.

    - Returns: sum of items at diagonal.
    */
    public func trace() -> Double{
        var total : Double = 0.0
        for i in 0..<self.__row{
            total += self.__values[i][i]
        }
        return total
    }

    /**
    The transpose method creates a new Matrix, then takes the transpose of values list
    and puts transposition to the Matrix.

    - Returns: Matrix type output.
    */
    public func transpose() -> Matrix{
        let result : Matrix = Matrix(row: self.__col, col: self.__row)
        for i in 0..<self.__row{
            for j in 0..<self.__col{
                result.__values[j][i] = self.__values[i][j]
            }
        }
        return result
    }

    /**
    The partial method takes 4 integer inputs; rowStart, rowEnd, colStart, colEnd and creates a Matrix size of
    rowEnd - rowStart + 1 x colEnd - colStart + 1. Then, puts corresponding items of values list
    to the new result Matrix.

    - Parameters:
        - rowStart : integer input for public funcining starting index of row.
        - rowEnd : integer input for public funcining ending index of row.
        - colStart : integer input for public funcining starting index of column.
        - colEnd : integer input for public funcining ending index of column.

    - Returns: result Matrix.
    */
    public func partial(rowStart: Int, rowEnd: Int, colStart: Int, colEnd: Int) -> Matrix{
        let result : Matrix = Matrix(row: rowEnd - rowStart + 1, col: colEnd - colStart + 1)
        for i in rowStart..<rowEnd + 1{
            for j in colStart..<colEnd + 1{
                result.__values[i - rowStart][j - colStart] = self.__values[i][j]
            }
        }
        return result
    }

    /**
    The isSymmetric method compares each item of values list at positions (i, j) with (j, i)
    and returns true if they are equal, false otherwise.

    - Returns: true if items are equal, false otherwise.
    */
    public func isSymmetric() -> Bool{
        for i in 0..<self.__row - 1{
            for j in 0..<self.__row{
                if self.__values[i][j] != self.__values[j][i]{
                    return false
                }
            }
        }
        return true
    }

    /**
    The determinant method first creates a new list, and copies the items of  values
    list into new list. Then, calculates the determinant of this
    new list.

    - Returns: determinant of values list.
    */
    public func determinant() -> Double{
        var det : Double = 1.0
        let copyOfMatrix : Matrix = self.copy() as! Matrix
        for i in 0..<self.__row{
            det *= copyOfMatrix.__values[i][i]
            if det == 0.0{
                break
            }
            for j in i + 1..<self.__row{
                let ratio : Double = copyOfMatrix.__values[j][i] / copyOfMatrix.__values[i][i]
                for k in i..<self.__col{
                    copyOfMatrix.__values[j][k] = copyOfMatrix.__values[j][k] - copyOfMatrix.__values[i][k] * ratio
                }
            }
        }
        return det
    }

    ///The inverse method finds the inverse of values list.
    public func inverse(){
        let b : Matrix = Matrix(row: self.__row, col: self.__row)
        var indxc : [Int] = []
        var indxr : [Int] = []
        var ipiv : [Int] = []
        for _ in 0..<self.__row{
            ipiv.append(0)
        }
        for _ in 1..<self.__row + 1{
            var big : Double = 0.0
            var irow : Int = -1
            var icol : Int = -1
            for j in 1..<self.__row + 1{
                if ipiv[j - 1] != 1{
                    for k in 1..<self.__row + 1{
                        if ipiv[k - 1] == 0{
                            if abs(self.__values[j - 1][k - 1]) >= big{
                                big = abs(self.__values[j - 1][k - 1])
                                irow = j
                                icol = k
                            }
                        }
                    }
                }
            }
            ipiv[icol - 1] = ipiv[icol - 1] + 1
            if irow != icol{
                for l in 1..<self.__row + 1{
                    let dum : Double = self.__values[irow - 1][l - 1]
                    self.__values[irow - 1][l - 1] = self.__values[icol - 1][l - 1]
                    self.__values[icol - 1][l - 1] = dum
                }
                for l in 1..<self.__row + 1{
                    let dum : Double = b.__values[irow - 1][l - 1]
                    b.__values[irow - 1][l - 1] = b.__values[icol - 1][l - 1]
                    b.__values[icol - 1][l - 1] = dum
                }
            }
            indxr.append(irow)
            indxc.append(icol)
            let pivinv : Double = 1.0 / self.__values[icol - 1][icol - 1]
            self.__values[icol - 1][icol - 1] = 1.0
            for l in 1..<self.__row + 1{
                self.__values[icol - 1][l - 1] = self.__values[icol - 1][l - 1] * pivinv
            }
            for l in 1..<self.__row + 1{
                b.__values[icol - 1][l - 1] = b.__values[icol - 1][l - 1] * pivinv
            }
            for ll in 1..<self.__row + 1{
                if ll != icol{
                    let dum : Double = self.__values[ll - 1][icol - 1]
                    self.__values[ll - 1][icol - 1] = 0.0
                    for l in 1..<self.__row + 1{
                        self.__values[ll - 1][l - 1] = self.__values[ll - 1][l - 1] - self.__values[icol - 1][
                            l - 1] * dum
                    }
                    for l in 1..<self.__row + 1{
                        b.__values[ll - 1][l - 1] = b.__values[ll - 1][l - 1] - b.__values[icol - 1][l - 1] * dum
                    }
                }
            }
        }
        var l : Int = self.__row;
        while l >= 1{
            if indxr[l - 1] != indxc[l - 1]{
                for k in 1..<self.__row + 1{
                    let dum : Double = self.__values[k - 1][indxr[l - 1] - 1]
                    self.__values[k - 1][indxr[l - 1] - 1] = self.__values[k - 1][indxc[l - 1] - 1]
                    self.__values[k - 1][indxc[l - 1] - 1] = dum
                }
            }
            l = l - 1
        }
    }

    /**
    The choleskyDecomposition method creates a new Matrix and puts the Cholesky Decomposition of values Array
    into this Matrix. Also, it throws MatrixNotSymmetric exception if it is not symmetric and
    MatrixNotPositiveDefinite exception if the summation is negative.

    - Returns: Matrix type output.
    */
    public func choleskyDecomposition() -> Matrix{
        let b : Matrix = Matrix(row: self.__row, col: self.__col)
        for i in 0..<self.__row{
            for j in i..<self.__row{
                var total : Double = self.__values[i][j]
                var k : Int = i - 1
                while k >= 0{
                    total -= self.__values[i][k] * self.__values[j][k]
                    k = k - 1
                }
                if i == j{
                    b.__values[i][i] = sqrt(total)
                } else {
                    b.__values[j][i] = total / b.__values[i][i]
                }
            }
        }
        return b
    }

    /**
    The rotate method rotates values list according to given inputs.

    - Parameters:
        - s : double input.
        - tau : double input.
        - i : integer input.
        - j : integer input.
        - k : integer input.
        - l : integer input.
    */
    private func __rotate(s: Double, tau: Double, i: Int, j: Int, k: Int, l: Int){
        let g : Double = self.__values[i][j]
        let h : Double = self.__values[k][l]
        self.__values[i][j] = g - s * (h + g * tau)
        self.__values[k][l] = h + s * (g - h * tau)
    }

    /**
    The characteristics method finds and returns a sorted list of Eigenvecto}s. And it throws
    MatrixNotSymmetric exception if it is not symmetric.

    - Returns: A sorted list of Eigenvectors.
    */
    public func characteristics() -> [Eigenvector]{
        let matrix1 : Matrix = self.copy() as! Matrix
        let v : Matrix = Matrix(size: self.__row)
        var d : [Double] = []
        var b : [Double] = []
        var z : [Double] = []
        let EPS : Double = 0.000000000000000001
        for ip in 0..<self.__row{
            b.append(matrix1.__values[ip][ip])
            d.append(matrix1.__values[ip][ip])
            z.append(0.0)
        }
        for i in 1..<51{
            var sm : Double = 0.0
            for ip in 0..<self.__row - 1{
                for iq in ip + 1..<self.__row{
                    sm += abs(matrix1.__values[ip][iq])
                }
            }
            if sm == 0.0{
                break
            }
            var threshold : Double
            if i < 4{
                threshold = 0.2 * sm / pow(Double(self.__row), 2.0)
            } else {
                threshold = 0.0
            }
            for ip in 0..<self.__row - 1{
                for iq in ip + 1..<self.__row{
                    let g : Double = 100.0 * abs(matrix1.__values[ip][iq])
                    if i > 4 && g <= EPS * abs(d[ip]) && g <= EPS * abs(d[iq]){
                        matrix1.__values[ip][iq] = 0.0
                    } else {
                        if abs(matrix1.__values[ip][iq]) > threshold{
                            var h : Double = d[iq] - d[ip]
                            var t : Double
                            if g <= EPS * abs(h){
                                t = matrix1.__values[ip][iq] / h
                            } else {
                                let theta : Double = 0.5 * h / matrix1.__values[ip][iq]
                                t = 1.0 / (abs(theta) + sqrt(1.0 + pow(theta, 2.0)))
                                if theta < 0.0{
                                    t = -t
                                }
                            }
                            let c : Double = 1.0 / sqrt(1 + pow(t, 2.0))
                            let s : Double = t * c
                            let tau : Double = s / (1.0 + c)
                            h = t * matrix1.__values[ip][iq]
                            z[ip] -= h
                            z[iq] += h
                            d[ip] -= h
                            d[iq] += h
                            matrix1.__values[ip][iq] = 0.0
                            for j in 0..<ip{
                                matrix1.__rotate(s: s, tau: tau, i: j, j: ip, k: j, l: iq)
                            }
                            for j in ip + 1..<iq{
                                matrix1.__rotate(s: s, tau: tau, i: ip, j: j, k: j, l: iq)
                            }
                            for j in iq + 1..<self.__row{
                                matrix1.__rotate(s: s, tau: tau, i: ip, j: j, k: iq, l: j)
                            }
                            for j in 0..<self.__row{
                                v.__rotate(s: s, tau: tau, i: j, j: ip, k: j, l: iq)
                            }
                        }
                    }
                }
            }
            for ip in 0..<self.__row{
                b[ip] = b[ip] + z[ip]
                d[ip] = b[ip]
                z[ip] = 0.0
            }
        }
        var result : [Eigenvector] = []
        for i in 0..<self.__row{
            if d[i] > 0{
                result.append(Eigenvector(eigenvalue: d[i], values: v.getColumnVector(column: i)))
            }
        }
        result.sort(by: {$0.getEigenvalue() > $1.getEigenvalue()})
        return result
    }

}

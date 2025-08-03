//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 16.08.2020.
//

import Foundation

public class Vector : Equatable{
    
    private var __size : Int
    private var values : [Double]

    /**
     * A constructor of {@link Vector} class which takes an {@link ArrayList} values as an input. Then, initializes
     * values {@link ArrayList} and size variable with given input and ts size.
     *
        - Parameter values : {@link ArrayList} input.
     */
    public init(values: [Double]) {
        self.values = values
        __size = values.count
    }


    /**
     * Another constructor of {@link Vector} class which takes integer size and double x as inputs. Then, initializes size
     * variable with given size input and creates new values {@link ArrayList} and adds given input x to values {@link ArrayList}.
     *
        - Parameters:
            - size: {@link ArrayList} size.
            - x : item to add values {@link ArrayList}.
     */
    public init(size: Int, x: Double) {
        self.__size = size
        values = []
        for _ in 0..<size{
            values.append(x)
        }
    }

    /**
     * Another constructor of {@link Vector} class which takes integer size, integer index and double x as inputs. Then, initializes size
     * variable with given size input and creates new values {@link ArrayList} and adds 0.0 to values {@link ArrayList}.
     * Then, sets the item of values {@link ArrayList} at given index as given input x.
     *
        - Parameters:
            - size: {@link ArrayList} size.
            - index: to set a particular item.
            - x : item to add values {@link ArrayList}'s given index.
     */
    public init(size: Int, index: Int, x: Double) {
        self.__size = size
        values = []
        for _ in 0..<size{
            values.append(0.0);
        }
        values[index] = x;
    }

    public static func == (lhs: Vector, rhs: Vector) -> Bool {
        if lhs.__size != rhs.__size{
            return false
        }
        for i in 0..<lhs.__size{
            if lhs.getValue(index: i) != rhs.getValue(index: i){
                return false
            }
        }
        return true
    }

    /**
    The biased method creates a list result, add adds each item of values list into the result list.
    Then, insert 1.0 to 0th position and return result list.

    - Returns: result list.
    */
    public func biased() -> Vector{
        let result : Vector = Vector(size: 0, x: 0)
        for value in self.values{
            result.add(x: value)
        }
        result.insert(pos: 0, x: 1.0)
        return result
    }

    /**
    The add method adds given input to the values {@link ArrayList} and increments the size variable by one.

    - Parameter x : input to add values list.
    */
    public func add(x: Double){
        self.values.append(x)
        self.__size = self.__size + 1
    }

    /**
    The insert method puts given input to the given index of values list and increments the size variable by one.

    PARAMETERS
    ----------
    pos : int
        index to insert input.
    x : double
        input to insert to given index of values list.
    */
    public func insert(pos: Int, x: Double){
        self.values.insert(x, at: pos)
        self.__size = self.__size + 1
    }

    /**
    The remove method deletes the item at given input position of values list and decrements the size variable by
    one.

    - Parameter pos : index to remove from values list.
    */
    public func remove(pos: Int){
        self.values.remove(at: pos)
        self.__size = self.__size - 1
    }

    ///The clear method sets all the elements of values list to 0.
    public func clear(){
        for i in 0..<self.values.count{
            self.values[i] = 0
        }
    }

    /**
    The sumOfElements method sums up all elements in the vector.

    - Returns: Sum of all elements in the vector.
    */
    public func sumOfElements() -> Double{
        var total : Double = 0.0
        for i in 0..<self.__size{
            total += self.values[i]
        }
        return total
    }

    /**
    The maxIndex method gets the first item of values list as maximum item, then it loops through the indices
    and if a greater value than the current maximum item comes, it updates the maximum item and returns the final
    maximum item's index.

    - Returns: final maximum item's index.
    */
    public func maxIndex() -> Int{
        var index : Int = 0
        var maxValue : Double = self.values[0]
        for i in 1..<self.__size{
            if self.values[i] > maxValue{
                maxValue = self.values[i]
                index = i
            }
        }
        return index
    }

    /**
    The sigmoid method loops through the values list and sets each ith item with sigmoid public function, i.e
    1 / (1 + Math.exp(-values.get(i))), i ranges from 0 to size.
    */
    public func sigmoid(){
        for i in 0..<self.__size{
            self.values[i] = 1 / (1 + exp(-self.values[i]))
        }
    }

    /**
     * The tanh method loops through the values {@link ArrayList} and sets each ith item with tanh function, i.e, i
     * ranges from 0 to size.
     */
    public func tanh(){
        for i in 0..<self.__size{
            self.values[i] = (exp(self.values[i]) - exp(-self.values[i])) / (exp(self.values[i]) + exp(-self.values[i]))
        }
    }

    /**
     * The relu method loops through the values {@link ArrayList} and sets each ith item with relu function, i.e, i
     * ranges from 0 to size.
     */
    public func relu(){
        for i in 0..<self.__size{
            if self.values[i] < 0{
                self.values[i] = 0.0
            }
        }
    }

    /**
     * The relu method loops through the values {@link ArrayList} and sets each ith item with the derivative of relu function, i.e, i ranges from 0 to size.
     */
    public func reluDerivative(){
        for i in 0..<self.__size{
            if self.values[i] > 0{
                self.values[i] = 1.0
            } else {
                self.values[i] = 0.0
            }
        }
    }

    /**
    The skipVector method takes a mod and a value as inputs. It creates a new result Vector, and assigns given input
    value to i. While i is less than the size, it adds the ith item of values {@link ArrayList} to the result and
    increments i by given mod input.

    - Parameters:
        - mod : integer input.
        - value : integer input.

    - Returns: result Vector.
    */
    public func skipVector(mod: Int, value: Int) -> Vector{
        let result : Vector = Vector(size: 0, x: 0)
        var i : Int = value
        while i < self.__size{
            result.add(x: self.values[i])
            i += mod
        }
        return result
    }

    /**
    The add method takes a Vector v as an input. It sums up the corresponding elements of both given vector's
    values list and values list and puts result back to the values list.

    - Parameter v : Vector to add.
    */
    public func addVector(v: Vector){
        for i in 0..<self.__size{
            self.values[i] = self.values[i] + v.values[i]
        }
    }

    /**
    The subtract method takes a Vector v as an input. It subtracts the corresponding elements of given vector's
    values list from values list and puts result back to the values list.

    - Parameter v : Vector to subtract from values list.
    */
    public func subtract(v: Vector){
        for i in 0..<self.__size{
            self.values[i] = self.values[i] - v.values[i]
        }
    }

    /**
    The difference method takes a Vector v as an input. It creates a new Vector result, then
    subtracts the corresponding elements of given vector's values list from values list and puts
    result back to the result.

    - Parameter v : Vector to find difference from values list.

    - Returns: new Vector with result list.
    */
    public func difference(v: Vector) -> Vector{
        let result : Vector = Vector(size: 0, x: 0)
        for i in 0..<self.__size{
            result.add(x: self.values[i] - v.values[i])
        }
        return result
    }

    /**
    The dotProduct method takes a Vector v as an input. It creates a new double variable result, then
    multiplies the corresponding elements of given vector's values list with values list and assigns
    the multiplication to the result.

    - Parameter v : Vector to find dot product.

    - Returns: result.
    */
    public func dotProduct(v: Vector) -> Double{
        var result : Double = 0
        for i in 0..<self.__size{
            result += self.values[i] * v.values[i]
        }
        return result
    }

    /**
    The dotProduct method creates a new double variable result, then squares the elements of values list and assigns
    the accumulation to the result.

    - Returns: result.
    */
    public func dotProductWithSelf() -> Double{
        var result : Double = 0
        for i in 0..<self.__size{
            result += self.values[i] * self.values[i]
        }
        return result
    }

    /**
    The elementProduct method takes a Vector v as an input. It creates a new Vector result, then
    multiplies the corresponding elements of given vector's values list with values list and adds
    the multiplication to the result list.

    - Parameter v : Vector to find dot product.

    - Returns: with result list.
    */
    public func elementProduct(v: Vector) -> Vector{
        let result : Vector = Vector(size: 0, x: 0)
        for i in 0..<self.__size{
            result.add(x: self.values[i] * v.values[i])
        }
        return result
    }

    /**
     * The multiply method takes a {@link Vector} v as an input and creates new {@link Matrix} m of [size x size of input v].
     * It loops through the the both values {@link ArrayList} and given vector's values {@link ArrayList}, then multiply
     * each item with other with other items and puts to the new {@link Matrix} m.
     - Parameters:
        - v: Vector input.
     - Returns: Matrix that has multiplication of two vectors.
     */
    public func multiply(v: Vector) -> Matrix{
        let m : Matrix = Matrix(row: __size, col: v.__size)
        for i in 0..<__size{
            for j in 0..<v.__size{
                m.setValue(rowNo: i, colNo: j, value: values[i] * v.values[j])
            }
        }
        return m
    }
    
    /**
    The divide method takes a double value as an input and divides each item of values list with given value.

    - Parameter value : is used to divide items of values list.
    */
    public func divide(value: Double){
        for i in 0..<self.__size{
            self.values[i] = self.values[i] / value
        }
    }

    /**
    The multiply method takes a double value as an input and multiplies each item of values list with given value.

    - Parameter value : is used to multiply items of values list.
    */
    public func multiply(value: Double){
        for i in 0..<self.__size{
            self.values[i] = self.values[i] * value
        }
    }

    /**
    The product method takes a double value as an input and creates a new result {@link Vector}, then multiplies
    each item of values list with given value and adds to the result {@link Vector}.

    - Parameter value : is used to multiply items of values list.

    - Returns: Vector result.
    */
    public func product(value: Double) -> Vector{
        let result : Vector = Vector(size: 0, x: 0)
        for i in 0..<self.__size{
            result.add(x: self.values[i] * value)
        }
        return result
    }

    /**
    The l1Normalize method is used to apply Least Absolute Errors, it accumulates items of values list and sets
    each item by dividing it by the summation value.
    */
    public func l1Normalize(){
        var total : Double = 0
        for i in 0..<self.__size{
            total += self.values[i]
        }
        for i in 0..<self.__size{
            self.values[i] = self.values[i] / total
        }
    }

    /**
    The l2Norm method is used to apply Least Squares, it accumulates second power of each items of values list
    and returns the square root of this summation.

    - Returns: square root of this summation.
    */
    public func l2Norm() -> Double{
        var total : Double = 0
        for i in 0..<self.__size{
            total += pow(self.values[i], 2.0)
        }
        return sqrt(total)
    }

    /**
    The cosineSimilarity method takes a Vector v as an input and returns the result of dotProduct(v)
    / l2Norm() / v.l2Norm().

    - Parameter v : input.

    - Returns: dotProduct(v) / l2Norm() / v.l2Norm()
    */
    public func cosineSimilarity(v: Vector) -> Double{
        return self.dotProduct(v: v) / self.l2Norm() / v.l2Norm()
    }

    /**
    The size method returns the size of the values list

    - Returns: size of the values list
    */
    public func size() -> Int{
        return self.values.count
    }

    /**
    Getter for the item at given index of values list

    - Parameter index : index used to get an item.

    - Returns: the item at given index.
    */
    public func getValue(index: Int) -> Double{
        return self.values[index]
    }

    /**
    Setter for the setting the value at given index of values list.

    - Parameters:
        - index : index to set.
        - value : is used to set the given index
    */
    public func setValue(index: Int, value: Double){
        self.values[index] = value
    }

    /**
    The addValue method adds the given value to the item at given index of values list.

    - Parameters:
        - index : index to add the given value.
        - value : value to add to given index.
    */
    public func addValue(index: Int, value: Double){
        self.values[index] += value
    }

}

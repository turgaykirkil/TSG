//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 12.08.2020.
//

import Foundation

public class RandomArray{

    /**
      The constructor of RandomNormalizedArray class gets an integer itemCount as an input. Creates a list of
      size itemCount and loops through each element of the list and initializes them with a random number by using
      random. Then, accumulates each element of the list and at the end divides each element with the resulting sum.
     
      - Parameter itemCount : input representing array size.
     */
    public static func normalizedArray(itemCount: Int) -> [Double]{
        var total = 0.0
        var array : [Double] = []
        let random = Random()
        for i in 0..<itemCount{
            array.append(random.nextDouble(min: 0, max: 1))
            total += array[i]
        }
        for i in 0..<itemCount{
            array[i] /= total
        }
        return array
    }

    /**
      Creates and returns a random index array, where the indexes in the array are between 0 and itemCount - 1. For
      example, if itemCount is 4, the method returns an array of indexes 0, 1, 2, 3 but shuffled.
      - Parameter itemCount: Number of indexes
      - Returns Shuffled array containing numbers between 0 and itemCount - 1.
     */
    public static func indexArray(itemCount: Int) -> [Int]{
        var array : [Int] = []
        for i in 0..<itemCount{
            array.append(i)
        }
        array.shuffle()
        return array
    }
}

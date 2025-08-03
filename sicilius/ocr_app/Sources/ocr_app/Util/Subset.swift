//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 12.08.2020.
//

import Foundation

public class Subset{
    
    var set: [Int]
    private var rangeEnd: Int
    var elementCount: Int

    /**
    The constructor of Subset class which takes 3 integer inputs; rangeStart, rangeEnd, and elementCount.
    It initializes variables rangeEnd and elementCount with given inputs, creates 2 arrays; set and multiset with
    the size of given elementCount and multisetCount, which is derived from elementCount, respectively. Then, it
    assigns rangeStart+i to each ith element of set.

    - Parameters:
        - rangeStart: input defining start range.
        - rangeEnd : input defining ending range.
        - elementCount : input element count.
    */
    public init(rangeStart: Int, rangeEnd: Int, elementCount: Int){
        self.rangeEnd = rangeEnd
        self.elementCount = elementCount
        self.set = []
        for i in 0..<elementCount{
            self.set.append(rangeStart + i)
        }
    }

    /**
    Getter for the set list

    - Returns: the set list
    */
    public func get() -> [Int]{
        return self.set
    }

    /**
    The next method generates the next subset.

    - Returns: true if next subset generation is possible, false otherwise.
    */
    public func next() -> Bool{
        var i: Int = self.elementCount - 1
        while i > -1{
            self.set[i] = self.set[i] + 1
            if self.set[i] <= self.rangeEnd - self.elementCount + i + 1{
                break
            }
            i = i - 1
        }
        if i == -1{
            return false
        }
        for j in i + 1..<self.elementCount{
            self.set[j] = self.set[j - 1] + 1
        }
        return true
    }

}

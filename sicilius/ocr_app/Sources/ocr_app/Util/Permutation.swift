//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 12.08.2020.
//

import Foundation

public class Permutation{

    private var a: [Int]
    private var n: Int
    
    /**
    A constructor of Permutation class which creates a new list and assigns integer
    numbers starting from 0 to given input n.

    - Parameter n: integer input.
    */
    public init(n: Int){
        self.n = n
        self.a = []
        for i in 0..<n{
            self.a.append(i)
        }
    }

    /**
     The get method returns the list a.

     - Returns: a
    */
    public func get() -> [Int]{
        return self.a
    }

    /**
     The next method generates next permutation for the list a.

     - Returns: true if next permutation is possible, false otherwise.
    */
    public func next() -> Bool{
        var i = self.n - 2
        while i >= 0 && self.a[i] >= self.a[i + 1]{
            i = i - 1
        }
        if i == -1 {
            return false
        }
        var j = self.n - 1
        while self.a[i] >= self.a[j]{
            j = j - 1
        }
        Swap.swap(a: &self.a, i: i, j: j)
        var k = i + 1
        j = self.n - 1
        while k < j{
            Swap.swap(a: &self.a, i: j, j: k)
            k = k + 1
            j = j - 1
        }
        return true
    }

}

//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 12.08.2020.
//

import Foundation

public class Swap{
    
    /**
    The swap method takes a list and two integer numbers i, j. And interchange the given array's
    items at index i and index j.

    - Parameters:
        - array : input
        - i : first index to swap.
        - j : second index to change.
    */
    static public func swap(a: inout [Int], i: Int, j: Int){
        let t = a[i]
        a[i] = a[j]
        a[j] = t
    }
    
}

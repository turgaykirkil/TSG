//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 12.08.2020.
//

import Foundation

public class Interval {
    
    private var list: [Tuple]
    
    /// A constructor of Interval class which creates a new list.
    public init(){
        self.list = []
    }

    /** The add method adds a new Tuple with given inputs to the list.

        - Parameters:
            - start : first element of Tuple.
            - end : second element of Tuple.
    */
    public func add(start: Int, end: Int){
        self.list.append(Tuple(first:start, last:end))
    }

    /** The getFirst method returns the first element at the list list's given index.

        - Parameter index : to use at getting tuple from list.
     
        - Returns: the first element at the list list's given index.
    */
    public func getFirst(index: Int) -> Int{
        return self.list[index].getFirst()
    }

    /** The getLast method returns the last element at the list list's given index.

        - Parameter index : to use at getting tuple from list.

        - Returns: the last element at the list list's given index.
    */
    public func getLast(index: Int) -> Int{
        return self.list[index].getLast()
    }

    /** The size method returns the size of the list list.
    
        - Returns: size of the list list.
    */
    public func size() -> Int{
        return self.list.count
    }

}

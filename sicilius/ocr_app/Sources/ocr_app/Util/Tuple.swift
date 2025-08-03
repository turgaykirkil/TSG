//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 12.08.2020.
//

import Foundation

public class Tuple{
    
    private var first: Int
    private var last: Int
    
    /**
    The constructor of {@link Tuple} class which takes two integer inputs and initializes first and last variables
    with given inputs.
     
     - Parameters:
        - first: first integer input.
        - last: integer input.
    */
    public init(first : Int, last : Int){
        self.first = first
        self.last = last
    }
    
    /**
    Getter for the first item at {@link Tuple}.

     - Returns: The first item.
    */
    public func getFirst()-> Int{
        return first
    }
    
    /**
    Getter for the last item at {@link Tuple}.

     - Returns: the last item.
     */
    public func getLast()-> Int {
        return last
    }
}

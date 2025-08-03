//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 6.09.2020.
//

import Foundation


public class VectorizedWord : Word{
    
    private var __vector: Vector

    /**
    A constructor of VectorizedWord class which takes a String and a Vector as inputs and calls its
    super class Word with name and also initializes vector variable with given input.

    - Parameters:
        - name : String input.
        - vector : Vector type input.
    */
    public init(name: String, vector: Vector){
        self.__vector = vector
        super.init(name: name)
    }

    /**
    Getter for the vector variable.

    - Returns: the vector variable.
    */
    public func getVector() -> Vector{
        return self.__vector
    }

}

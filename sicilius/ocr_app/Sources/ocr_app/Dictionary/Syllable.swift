//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 6.09.2020.
//

import Foundation

public class Syllable{
    
    private var __syllable: String

    /**
    A conStringuctor of Syllable class which takes a String as an input and initializes syllable variable with given input.

    - Parameter syllable : String input.
    */
    public init(syllable: String){
        self.__syllable = syllable
    }

    /**
    Getter for the syllable variable.

    - Returns: The syllable variable.
    */
    public func getText() -> String{
        return self.__syllable
    }

}

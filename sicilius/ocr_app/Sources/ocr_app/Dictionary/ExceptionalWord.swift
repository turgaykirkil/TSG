//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 6.09.2020.
//

import Foundation

public class ExceptionalWord : Word{
    
    private var __root: String
    private var __pos: Pos

    /**
    A constructor of ExceptionalWord class which takes a Pos as a  part of speech and two Strings; name
    and root as inputs. Then, calls its super class Word with given name and initialises root and pos variables
    with given inputs.

    - Parameters:
        - name : String input.
        - root : String input.
        - pos : Pos type input.
    */
    public init(name: String, root: String, pos: Pos){
        self.__root = root
        self.__pos = pos
        super.init(name: name)
    }

    /**
    Getter for the root variable.

    - Returns: root variable.
    */
    public func getRoot() -> String{
        return self.__root
    }

    /**
    Getter for the pos variable.

    - Returns: pos variable.
    */
    public func getPos() -> Pos{
        return self.__pos
    }
    
}

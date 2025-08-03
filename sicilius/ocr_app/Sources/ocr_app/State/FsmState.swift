//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 3.03.2021.
//

import Foundation

public class FsmState : Hashable{
    
    public static func == (lhs: FsmState, rhs: FsmState) -> Bool {
        return lhs.__name == rhs.__name
    }
    
    public func hash(into hasher: inout Hasher) {
        hasher.combine(__name)
    }
    
    private var __startState: Bool
    private var __endState: Bool
    private var __name: String
    private var __pos: String?
    
    /**
    First constructor of the {@link State} class which takes 3 parameters String name, boolean startState,
    and boolean endState as input and initializes the private variables of the class also leaves pos as null.
     
    - Parameters:
        - name: String input.
        - startState: boolean input.
        - endState: boolean input.
     */
    public init(name: String, startState: Bool, endState: Bool){
        self.__name = name;
        self.__startState = startState;
        self.__endState = endState;
        self.__pos = nil;
    }

    /**
    Second constructor of the {@link State} class which takes 4 parameters as input; String name, boolean startState,
    boolean endState, and String pos and initializes the private variables of the class.

     - Parameters:
        - name: String input.
        - startState: boolean input.
        - endState:  boolean input.
        - pos:        String input.
     */
    public init(name: String, startState: Bool, endState: Bool, pos: String){
        self.__name = name;
        self.__startState = startState;
        self.__endState = endState;
        self.__pos = pos;
    }
    
    /**
    Getter for the name.

     - Returns: String name.
     */
    public func getName() -> String{
        return self.__name
    }

    /**
    Getter for the pos.

     - Returns: String pos.
     */
    public func getPos() -> String?{
        return self.__pos
    }

    /**
    The isEndState method returns endState's value.

     - Returns: boolean endState.
     */
    public func isEndState() -> Bool{
        return self.__endState
    }
    
    public func description() -> String{
        return self.__name
    }

}

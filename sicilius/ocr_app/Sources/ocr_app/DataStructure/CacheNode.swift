//
//  CacheNode.swift
//  
//
//  Created by Olcay Taner YILDIZ on 14.08.2020.
//

import Foundation

public class CacheNode<K, T>{
    private var key: K
    private var data: T
    private var previous: CacheNode? = nil
    private var next: CacheNode? = nil

    /**
    A constructor of CacheNode class which takes a key and a data as inputs and initializes private fields with
    these inputs.

     - Parameters:
        - key : K type input for representing keys.
        - data : T type input values represented by keys.
    */
    init(key: K, data: T){
        self.key = key
        self.data = data
        self.previous = nil
        self.next = nil
    }

    /**
    Getter for data value.

    - Returns: data value.
    */
    public func getData() -> T{
        return self.data
    }

    /**
    Getter for key value.

    - Returns: key value.
    */
    public func getKey() -> K{
        return self.key
    }

    /**
    Getter for the previous CacheNode.

    - Returns: previous CacheNode.
    */
    public func getPrevious() -> CacheNode?{
        return self.previous
    }

    /**
    Getter for the next CacheNode.

    - Returns: next CacheNode.
    */
    public func getNext() -> CacheNode?{
        return self.next
    }

    /**
    Setter for the previous CacheNode.

    - Parameter previous : previous CacheNode.
    */
    public func setPrevious(previous: CacheNode?){
        self.previous = previous
    }

    /**
    Setter for the next CacheNode.

    - Parameter: next : next CacheNode.
    */
    public func setNext(next: CacheNode){
        self.next = next
    }

}

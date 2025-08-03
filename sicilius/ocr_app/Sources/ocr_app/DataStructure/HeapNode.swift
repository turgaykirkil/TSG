//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 13.10.2022.
//

import Foundation

public class HeapNode<T>{
    
    var data: T
    
    /// Constructor of HeapNode.
    /// - Parameter data: Data to be stored in the heap node.
    public init(data: T){
        self.data = data
    }
    
    /// Mutator of the data field
    /// - Returns: Data
    public func getData()-> T{
        return self.data
    }
}

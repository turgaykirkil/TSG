//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 4.07.2022.
//

import Foundation

public class TreeNode<T>{
    
    var data: T
    var left: TreeNode<T>? = nil
    var right: TreeNode<T>? = nil
    
    public init(data: T){
        self.data = data
    }
}

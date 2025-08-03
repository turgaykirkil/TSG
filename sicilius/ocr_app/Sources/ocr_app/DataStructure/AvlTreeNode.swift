//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 4.07.2022.
//

import Foundation

public class AvlTreeNode<T> : TreeNode<T>{
    
    var height: Int
    
    public override init(data: T) {
        self.height = 1
        super.init(data: data)
    }
}

//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 13.10.2022.
//

import Foundation

public class MaxHeap<T : Comparable> : Heap<T>{
    
    public override init(N: Int){
        super.init(N: N)
    }
    
    public override func compare(data1: T, data2: T)-> Bool{
        return data1 < data2
    }
    
}

//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 12.08.2020.
//

import Foundation

public class SubsetFromList: Subset{

    private var elementList: [Int]
    private var indexList: [Int]

    /**
    A constructor of SubsetFromList class takes an integer list and an integer elementCount as inputs. It
    initializes elementList and elementCount variables with given inputs, then creates 3 arrays; set,indexList, and
    multiset with the size of given elementCount and multisetCount, which is derived from elementCount,
    respectively. Then, it assigns i to each ith element of indexList list and use this index to point at
    elementList and assigns to set list.

    - Parameters:
        - _list : list type input.
        - elementCount : input element count.
    */
    public init(_list: [Int], elementCount: Int){
        self.elementList = _list
        self.indexList = []
        super.init(rangeStart: 0, rangeEnd: 0, elementCount: 0)
        self.elementCount = elementCount
        self.set = []
        for i in 0..<elementCount{
            self.indexList.append(i)
            self.set.append(self.elementList[self.indexList[i]])
        }
    }

    /**
    The next method generates the next subset from list.

    - Returns: true if next subset generation from list is possible, false otherwise.
    */
    override public func next() -> Bool{
        var i : Int = self.elementCount - 1
        while i > -1{
            self.indexList[i] = self.indexList[i] + 1
            if self.indexList[i] < self.elementList.count - self.elementCount + i + 1{
                break
            }
            i = i - 1
        }
        if i == -1{
            return false
        }
        self.set[i] = self.elementList[self.indexList[i]]
        for j in i + 1..<self.elementCount{
            self.indexList[j] = self.indexList[j - 1] + 1
            self.set[j] = self.elementList[self.indexList[j]]
        }
        return true
    }

}

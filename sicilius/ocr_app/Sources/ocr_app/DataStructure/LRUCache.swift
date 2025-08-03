//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 14.08.2020.
//

import Foundation

public class LRUCache<K: Hashable, T>{
    
    private var cacheSize: Int
    private var map: [K : CacheNode<K, T>]
    private var cache: CacheLinkedList<K, T>

    /**
    A constructor of LRUCache class which takes cacheSize as input. It creates new CacheLinkedList and
    HashMap.

    - Parameter cacheSize : Integer input public funcining cache size.
    */
    public init(cacheSize: Int){
        self.cacheSize = cacheSize
        self.cache = CacheLinkedList<K, T>()
        self.map = [:]
    }

    /**
    The contains method takes a object type input key and returns true if the dictionary has the given key, false
    otherwise.

    - Parameter key : object type input key.

    - Returns: true if the HashMap has the given key, false otherwise.
    */
    public func contains(key: K) -> Bool{
        return self.map[key] != nil
    }

    /**
    The get method takes object type input key and returns the least recently used value. First it checks whether the
    dictionary has the given key, if so it gets the corresponding cacheNode. It removes that cacheNode from
    LinkedList and adds it again to the beginning of the list since it is more likely to be used again. At the end,
    returns the data value of that cacheNode.

    - Parameter key : object type input key.

    - Returns: data value if the dictionary has the given key, None otherwise.
    */
    public func get(key: K) -> T?{
        if self.map[key] != nil{
            let cacheNode : CacheNode<K, T> = self.map[key]!
            self.cache.removeGiven(cacheNode: cacheNode)
            self.cache.add(cacheNode: cacheNode)
            return cacheNode.getData()
        } else{
            return nil
        }
    }

    /**
    The add method take a key and a data as inputs. First it checks the size of the dictionary, if it is full (i.e
    equal to the given cacheSize) then it removes the last cacheNode in the list. If it has space for new entries,
    it creates new cacheNode with given inputs and adds this cacheNode to the linked list and also puts
    it to the dictionary.

    - Parameters:
        - key : object type input.
        - data : object type input
    */
    public func add(key: K, data: T){
        if self.map.count == self.cacheSize{
            let removed : CacheNode<K, T> = self.cache.remove()
            self.map[removed.getKey()] = nil
        }
        let cacheNode : CacheNode<K, T> = CacheNode(key: key, data: data)
        self.cache.add(cacheNode: cacheNode)
        self.map[key] = cacheNode
    }

}

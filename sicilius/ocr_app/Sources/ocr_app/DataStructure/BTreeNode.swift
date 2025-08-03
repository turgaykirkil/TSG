//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 4.07.2022.
//

import Foundation

public class BTreeNode<T : Comparable>{
    
    var K : [T]
    var m : Int
    var d : Int
    var leaf : Bool
    var children : [BTreeNode<T>]
    
    /// Constructor of the B+ Tree node. By default, it is a leaf node. Initializes the attributes.
    /// - Parameter d: d in d-ary tree.
    public init(d: Int){
        m = 0
        self.d = d
        leaf = true
        K = []
        children = []
    }
    
    /// Another constructor of a B+ Tree node. By default, it is not a leaf node. Adds two children.
    /// - Parameters:
    ///   - d: d in d-ary tree.
    ///   - firstChild: First child of the root node.
    ///   - secondChild: Second child of the root node.
    ///   - newK: First value in the node.
    public convenience init(d: Int, firstChild: BTreeNode<T>, secondChild: BTreeNode<T>, newK: T){
        self.init(d: d)
        leaf = false
        m = 1
        children.append(firstChild)
        children.append(secondChild)
        K.append(newK)
    }
    
    /// Searches the position of value in the list K. If the searched value is larger than the last value of node, we
    /// need to continue the search with the rightmost child. If the searched value is smaller than the i. value of node,
    /// we need to continue the search with the i. child.
    /// - Parameter value: Searched value
    /// - Returns: The position of searched value in array K.
    func position(value: T) -> Int{
        if m == 0{
            return 0
        }
        if value > K[m - 1]{
            return m
        } else {
            for i in 0..<m{
                if value <= K[i]{
                    return i
                }
            }
        }
        return -1
    }
    
    /// Add the new value insertedK to the array K into the calculated position index.
    /// - Parameters:
    ///   - index: Place to insert new value
    ///   - insertedK: New value to be inserted.
    private func insertIntoK(index: Int, insertedK: T){
        if index < K.count{
            for i in stride(from: m, to: index, by: -1){
                K[i] = K[i - 1]
            }
            K[index] = insertedK
        } else {
            K.append(insertedK)
        }
    }
    
    /// Transfers the last d values of the current node to the newNode.
    /// - Parameter newNode: New node.
    private func moveHalfOfTheKToNewNode(newNode: BTreeNode<T>){
        for i in 0..<d{
            newNode.K.append(K[i + d + 1])
        }
        newNode.m = d
    }
    
    /// Transfers the last d links of the current node to the newNode.
    /// - Parameter newNode: New node.
    private func moveHalfOfTheChildrenToNewNode(newNode: BTreeNode<T>){
        for i in 0..<d{
            newNode.children.append(children[i + d + 1])
        }
    }
    
    /// Transfers the last d values and the last d links of the current node to the newNode.
    /// - Parameter newNode: New node.
    private func moveHalfOfTheElementsToNewNode(newNode: BTreeNode<T>){
        moveHalfOfTheKToNewNode(newNode: newNode)
        moveHalfOfTheChildrenToNewNode(newNode: newNode)
    }
    
    /// First the function position is used to determine the node or the subtree to which the new node will be added.
    /// If this subtree is a leaf node, we call the function insertLeaf that will add the value to a leaf node. If this
    /// subtree is not a leaf node the function calls itself with the determined subtree. Both insertNode and insertLeaf
    /// functions, if adding a new value/node to that node/subtree necessitates a new child node to be added to the
    /// parent node, they will both return the new added node and the node obtained by dividing the original node. If
    /// there is not such a restructuring, these functions will return null. If we add a new child node to the parent
    /// node, first we open a space for that child node in the value array K, then we add this new node to the array K.
    /// After adding there are two possibilities:
    /// (i) After inserting the new child node, the current node did not exceed its capacity. In this case, we open
    ///     space for the link, which points to the new node, in the array children and place that link inside of this
    ///     array.
    /// (ii) After inserting the new child node, the current node exceed its capacity. In this case, we need to create
    ///     newNode, transfer the last d values and the last d links of the current node to the newNode. As a last case,
    ///     if the divided node is the root node, we need to create a new root node and the first child of this new root
    ///     node will be b, and the second child of the new root node will be newNode.
    /// - Parameters:
    ///   - value: Value to be inserted into B+ tree.
    ///   - isRoot: If true, value is inserted as a root node, otherwise false.
    /// - Returns: If inserted node results in a creation of a node, the function returns that node, otherwise null.
    public func insertNode(value: T, isRoot: Bool) -> BTreeNode<T>?{
        let child = position(value: value)
        var s: BTreeNode<T>?
        var newNode: BTreeNode<T>
        if !children[child].leaf{
            s = children[child].insertNode(value: value, isRoot: false)
        } else {
            s = children[child].insertLeaf(value: value)
        }
        if s == nil{
            return nil
        }
        insertIntoK(index: child, insertedK: children[child].K[d])
        if m < 2 * d{
            children.append(s!)
            m = m + 1
            return nil
        } else {
            newNode = BTreeNode(d: d)
            newNode.leaf = false
            moveHalfOfTheKToNewNode(newNode: newNode)
            newNode.children.append(s!)
            m = d
            if isRoot{
                return BTreeNode(d: d, firstChild: self, secondChild: newNode, newK: self.K[d])
            } else {
                return newNode
            }
        }
    }
    
    /// First the function position is used to determine the position where the new value will be placed Then we open a
    /// space for that value in the value array K, then we add this new value to the array K into the calculated
    /// position. At this stage there are again two possibilities:
    /// (i) After inserting the new value, the current leaf node did not exceed its capacity. The function returns
    /// null.
    /// (ii) After inserting the new value, the current leaf node exceed its capacity. In this case, we need to create
    /// the newNode, and transfer the last d values of node b to this newNode.
    /// - Parameter value: Value to be inserted into B+ tree.
    /// - Returns: If inserted node results in a creation of a node, the function returns that node, otherwise null.
    public func insertLeaf(value: T) -> BTreeNode<T>?{
        let child = position(value: value)
        insertIntoK(index: child, insertedK: value)
        if m < 2 * d{
            m = m + 1
            return nil
        } else {
            let newNode = BTreeNode(d: d)
            moveHalfOfTheKToNewNode(newNode: newNode)
            m = d
            return newNode
        }
    }
}

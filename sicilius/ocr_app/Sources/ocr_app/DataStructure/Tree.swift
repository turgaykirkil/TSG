//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 4.07.2022.
//

import Foundation

/// Tree structure is also a non-linear data structure. Different from the tree structure we see in the nature, the
/// tree data structure has its root on top and develops its branches down.
/// - Parameter T: Type of the data stored in the tree node.
public class Tree<T : Comparable>{
    
    var root: TreeNode<T>? = nil
    
    /// Constructor of the tree. According to the comparator, the tree could contain any object.
    public init(){
        
    }
    
    /// The search starts from the root node, and we represent the node, with which we compare the searched value, with
    /// d. If the searched value is equal to the value of the current node, we have found the node we search for, the
    /// function will return that node. If the searched value is smaller than the value of the current node , the number
    /// we search for must be on the left subtree of the current node, therefore the new current node must be the left
    /// child of the current node. As the last case, if the searched value is larger than the value of the current node,
    /// the number we search for must be on the right subtree of the current node, therefore the new current node must be
    /// the right child of the current node. If this search continues until the leaf nodes of the tree and we can't find
    /// the node we search for, node d will be null and the function will return null.
    /// - Parameter value: Searched value
    /// - Returns: If the value exists in the tree, the function returns the node that contains the node. Otherwise, it returns null.
    public func search(value: T)-> TreeNode<T>?{
        var d : TreeNode<T>? = root
        while d != nil{
            if d?.data == value{
                return d
            } else {
                if d!.data > value{
                    d = d?.left
                } else {
                    d = d?.right
                }
            }
        }
        return nil
    }
    
    /// Inserts a child to its parent as left or right child.
    /// - Parameters:
    ///   - parent: New parent of the child node.
    ///   - child: Child node.
    internal func insertChild(parent: TreeNode<T>?, child: TreeNode<T>){
        if parent == nil{
            root = child
        } else {
            if child.data < parent!.data{
                parent?.left = child
            } else {
                parent?.right = child
            }
        }
    }
    
    /// In order to add a new node into a binary search tree, we need to first find out the place where we will insert
    /// the new node. For this, we start from the root node and traverse the tree down. At each step, we compare the
    /// value of the new node with the value of the current node. If the value of the new node is smaller than the value
    /// of the current node, the new node will be inserted into the left subtree of the current node. To accomplish this,
    /// we continue the process with the left child of the current node. If the situation is reverse, that is, if the
    /// value of the new node is larger than the value of the current node, the new node will be inserted into the right
    /// subtree of the current node. In this case, we continue the process with the right child of the current node.
    /// - Parameter node: Node to be inserted.
    public func insert(node: TreeNode<T>){
        var y : TreeNode<T>? = nil
        var x : TreeNode<T>? = root
        while x != nil{
            y = x
            if node.data < x!.data{
                x = x?.left
            } else {
                x = x?.right
            }
        }
        insertChild(parent: y, child: node)
    }
    
    public func insert(data: T){
        insert(node: TreeNode(data: data))
    }
}

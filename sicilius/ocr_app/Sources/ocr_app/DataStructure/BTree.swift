//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 4.07.2022.
//

import Foundation

/// In the computer science literature, the structures such as AVL tree, splay tree, red-black tree are proposed, which
/// show the search tree property and also remain balanced after insertion and deletion operations.
/// Another possibility of constructing a balanced tree structure is to store not only a single value but more than one
/// value in a node. These type of tree structures are generalizations of the binary trees and called d-ary tree
/// structures in the computer science literature. 2-3-4 trees, B-tree, B+ trees can be given as example d-ary tree
/// structures. B+ trees, is one of the d-ary tree structures and used often in database systems.
/// B+ tree is a dynamic search tree structure and consists of two parts, an index part and a data part. The index part
/// is of d-ary tree structure, each node stores d < m < 2d values. d is a parameter of B+ tree, shows the capacity of B+
/// tree and called as the degree of the tree. The root node is the single exception to this rule and can store
/// 1 < m < 2d values. Each node also contains m + 1 links to point to its m + 1 child nodes. With the help of these
/// links, the tree can be traversed in top-down manner. Let Pi represent the link pointing to the node i and Ki
/// represent the i'th value in the same node, the i'th child and the ascendants of this child can take values between
/// the interval Ki < K < Ki+1. The data are stored in the leaf nodes and due to the definition of a tree, the leaf nodes
/// can not have children.
/// - Parameter T: Type of the data stored in the B tree node.
public class BTree<T : Comparable>{
    
    var root : BTreeNode<T>? = nil
    var d : Int
    
    /// Constructor of the tree. According to the comparator, the tree could contain any object.
    /// - Parameter d: Parameter d in d-ary tree.
    public init(d: Int){
        self.d = d
    }
    
    /// We start searching from the root node, the node with which we compare the searched value at each stage is
    /// represented by b, and we continue the search until we arrive the leaf nodes. In order to understand the subtree
    /// of node b where our searched value resides, we need to compare the searched value with the values Ki. For this,
    /// the function named position is given. If the searched value is larger than the last value of node b, we need to
    /// continue the search with the rightmost child. If the searched value is smaller than the i. value of node b, we
    /// need to continue the search with the i. child. As a last step, the function returns the leaf node of node b.
    /// - Parameter value: Value searched in B+ tree.
    /// - Returns: If the value exists in the tree, the function returns the node that contains the node. Otherwise, it returns null.
    public func search(value: T) -> BTreeNode<T>?{
        var b : BTreeNode<T>?
        var child : Int
        b = root
        while !b!.leaf{
            child = (b?.position(value: value))!
            if child < b!.m && b?.K[child] == value{
                return b
            }
            b = b?.children[child]
        }
        child = (b?.position(value: value))!
        if child < b!.m && b!.K[child] == value{
            return b
        }
        return nil
    }
    
    public func insert(data: T){
        if root == nil{
            root = BTreeNode(d: d)
        }
        if ((root?.leaf) != nil){
            let s = root?.insertLeaf(value: data)
            if s != nil{
                let tmp = root
                root = BTreeNode(d: d, firstChild: tmp!, secondChild: s!, newK: tmp!.K[d])
            }
        } else {
            let s = root?.insertNode(value: data, isRoot: true)
            if s != nil{
                root = s
            }
        }
    }
}

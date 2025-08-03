//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 4.07.2022.
//

import Foundation

///  AVL (Adelson-Velskii and Landis) tree is a balanced binary search tree structure. The balance property is very simple
/// and ensures the depth of the tree is in the level of O(log N).</p>
///
/// In AVL tree, the heights of the left and right subtrees of each node can differ by at most 1. If the heights of the
/// left and right subtrees of a single node differ by more than 1, then that binary search tree is not an AVL tree.</p>
/// - Parameter T: Type of the data stored in the tree node.

public class AvlTree<T : Comparable> : Tree<T>{
    
    public override init() {
    }
    
    public func height(d: AvlTreeNode<T>?) -> Int{
        if d == nil{
            return 0
        } else {
            return d!.height
        }
    }
    
    /// In rotate left, we move node k1 one level up, since due to the binary search tree
    /// property k2 > k1, we move node k2 one level down. The links updated are:
    /// (i) Since k2 > B > k1, the left child of node k2 is now the old right child of k1.
    /// (ii) The right child of k1 is now k2.
    /// Note that, the root node of the subtree is now k1. In order to modify the parent link of k2, the new root of the
    /// subtree is returned by the function.
    /// - Parameter k2: Root of the subtree, which does not satisfy the AVL tree property.
    /// - Returns: The new root of the subtree
    public func rotateLeft(k2: AvlTreeNode<T>) -> AvlTreeNode<T>{
        let k1 = k2.left as? AvlTreeNode<T>
        k2.left = k1?.right
        k1?.right = k2
        k2.height = max(height(d: k2.left as? AvlTreeNode<T>), height(d: k2.right as? AvlTreeNode<T>)) + 1
        k1?.height = max(height(d: k1?.left as? AvlTreeNode<T>), height(d: k1?.right as? AvlTreeNode<T>)) + 1
        return k1!
    }
    
    /// In order to restore the AVL tree property, we move node k2 one level up, since due to the binary search tree
    /// property k2 > k1, we move node k1 one level down. The links updated are:
    /// (i) Since k2 > B > k1, the right child of node k1 is now the old left child of k2.
    /// (ii) The left child of k2 is now k1
    /// Note that, the root node of the subtree is now k2. In order to modify the parent link of k1, the new root of the
    /// subtree is returned by the function.
    /// - Parameter k1: Root of the subtree, which does not satisfy the AVL tree property.
    /// - Returns: The new root of the subtree
    public func rotateRight(k1: AvlTreeNode<T>) -> AvlTreeNode<T>{
        let k2 = k1.right as? AvlTreeNode<T>
        k1.right = k2?.left
        k2?.left = k1
        k2!.height = max((k2!.left as! AvlTreeNode<T>).height, height(d: k2?.right as? AvlTreeNode<T>)) + 1
        k1.height = max(height(d: k1.left as? AvlTreeNode<T>), height(d: k1.right as? AvlTreeNode<T>)) + 1
        return k2!
    }
    
    /// In the first phase we will do single right rotation on the subtree rooted with k1. With this rotation, the left
    /// child of node k2 will be k1, whereas the right child of node k1 will be B (the old left child of node k2).
    /// In the second phase, we will do single left rotation on the subtree rooted with k3. With this rotation, the
    /// right child of node k2 will be k3, whereas the left child of node k3 will be C (the old right child of k2).
    /// Note that, the new root node of the subtree is now k2. In order to modify the parent link of k3, the new root of
    /// the subtree is returned by the function.
    /// - Parameter k3: Root of the subtree, which does not satisfy the AVL tree property.
    /// - Returns: The new root of the subtree
    public func doubleRotateLeft(k3: AvlTreeNode<T>) -> AvlTreeNode<T>{
        k3.left = rotateRight(k1: k3.left as! AvlTreeNode<T>)
        return rotateLeft(k2: k3)
    }
    
    /// In the first phase we will do single right rotation on the subtree rooted with k3. With this rotation, the right
    /// child of node k2 will be k3, whereas the left child of node k3 will be C (the old right child of node k2).
    /// In the second phase, we will do single right rotation on the subtree rooted with k1. With this rotation, the left
    /// child of node k2 will be k1, whereas the left child of node k1 will be B (the old left child of k2).</p>
    /// Note that, the new root node of the subtree is now k2. In order to modify the parent link of k1, the new root of
    /// the subtree is returned by the function.
    /// - Parameter k1: Root of the subtree, which does not satisfy the AVL tree property.
    /// - Returns: The new root of the subtree
    public func doubleRotateRight(k1: AvlTreeNode<T>) -> AvlTreeNode<T>{
        k1.right = rotateLeft(k2: k1.right as! AvlTreeNode<T>)
        return rotateRight(k1: k1)
    }
    
    /// First we will proceed with the stages the same when we add a new node into a binary search tree. For this, we
    /// start from the root node and traverse in down manner. The current node we visit is represented with x and the
    /// previous node is represented with y. At each time we compare the value of the current node with the value of the
    /// new node. If the value of the new node is smaller than the value of the current node, the new node will be
    /// inserted into the left subtree of the current node. For this, we will continue with the left child to process. If
    /// the reverse is true, that is, if the value of the new node is larger than the value of the current node, the new
    /// node will be inserted into the right subtree of the current node. In this case, we will continue with the right
    /// child to process. At each step, we store the current node in a separate stack.
    /// When we insert a new node into an AVL tree, we need to change the heights of the nodes and check if the AVL tree
    /// property is satisfied or not. Only the height of the nodes, which we visit while we are finding the place for the
    /// new node, can be changed. So, what we should do is to pop those nodes from the stack one by one and change the
    /// heights of those nodes.
    /// Similarly, the nodes, which we visit while we are finding the place for the new node, may no longer satisfy the
    /// AVL tree property. So what we should do is to pop those nodes from the stack one by one and calculate the
    /// difference of the heights of their left and right subtrees. If the height difference is 2, the AVL tree property
    /// is not satisfied. If we added the new node into the left subtree of the left child, we need to do left single
    /// rotation, if we added into the right subtree of the left child, we need to do left double rotation, if we added
    /// into the left subtree of the right child, we need to do right double rotation, if we added into the right subtree
    /// of the right child, we need to the right single rotation. Since  the root node of the subtree will be changed
    /// after a rotation, the new child of y will be the new root node t.
    /// - Parameter node: Node to be inserted.
    public func insert(node: AvlTreeNode<T>){
        let LEFT = 1, RIGHT = 2
        var y : AvlTreeNode<T>? = nil
        var x : AvlTreeNode<T>? = (root as? AvlTreeNode<T>)
        var t : AvlTreeNode<T>
        var dir1 : Int = 0, dir2 : Int = 0
        let c : Stack<AvlTreeNode<T>> = Stack()
        while x != nil{
            y = x
            c.push(item: y!)
            dir1 = dir2
            if node.data < x!.data{
                x = x!.left as? AvlTreeNode<T>
                dir2 = LEFT
            } else {
                x = x!.right as? AvlTreeNode<T>
                dir2 = RIGHT
            }
        }
        insertChild(parent: y, child: node)
        while !c.isEmpty(){
            x = c.pop()
            x?.height = max(height(d: (x?.left as? AvlTreeNode<T>)), height(d: (x?.right as? AvlTreeNode<T>))) + 1
            if abs(height(d: (x?.left as? AvlTreeNode<T>)) - height(d: (x?.right as? AvlTreeNode<T>))) == 2{
                if dir1 == LEFT{
                    if dir2 == LEFT{
                        t = rotateLeft(k2: x!)
                    } else {
                        t = doubleRotateLeft(k3: x!)
                    }
                } else {
                    if dir2 == LEFT{
                        t = doubleRotateRight(k1: x!)
                    } else {
                        t = rotateRight(k1: x!)
                    }
                }
                y = c.pop()
                insertChild(parent: y, child: t)
                break
            }
        }
    }
    
    public func insert(item: T){
        insert(node: AvlTreeNode<T>(data: item))
    }

}

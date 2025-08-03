//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 13.10.2022.
//

import Foundation

///
/// The heap data structure is a binary tree structure consisting of N elements. It shows the basic properties of the
/// binary tree data structure. The heap has a root node and each node of it has at most two child nodes
/// (left and right). The root node of the tree is shown at the top, and its branches grow not to up but to down manner.
///
/// In a heap, if the maximum element is in the root node and all nodes are smaller than its descendants, then this heap
/// is called max-heap, if the minimum element is in the root node and all nodes are larger than its descendants, then
/// this heap is called min-heap.
/// @param T: Type of the data stored in the heap node.

public class Heap<T : Comparable>{
    
    var array: [HeapNode<T>] = []
    var count: Int = 0
    
    /// Constructor of the heap. According to the comparator, the heap could be min or max heap.
    /// - Parameter N: Maximum number of elements in the heap.
    public init(N: Int){
    }
    
    /// Checks if the heap is empty or not.
    /// - Returns: True if the heap is empty, false otherwise.
    public func isEmpty()->Bool{
        return count == 0
    }
    
    /// Swaps two heap nodes in the heap given their indexes.
    /// - Parameters:
    ///   - index1: Index of the first node to swap.
    ///   - index2: Index of the second node to swap.
    public func swapNode(index1: Int, index2: Int){
        let tmp = array[index1]
        array[index1] = array[index2]
        array[index2] = tmp
    }
    
    public func compare(data1: T, data2: T)-> Bool{
        return data1 < data2
    }
    
    /// The function percolates down from a node of the tree to restore the max-heap property. Left or right children are
    /// checked, if one of them is larger than the current element of the heap, the iteration continues. The iteration is,
    /// determining the largest one of the node's children and switching that node's value with the current node's value.
    /// We need to check if current node's left and right children exist or not. These checks are done with for the left
    /// child and with for the right child.
    /// - Parameter n: Index of the starting node to restore the max-heap property.
    private func percolateDown(n: Int){
        var no : Int = n
        var left : Int = 2 * no + 1
        var right : Int = 2 * no + 2
        while ((left < count && compare(data1: array[no].getData(), data2: array[left].getData())) ||
               (right < count && compare(data1: array[no].getData(), data2: array[right].getData()))){
            if (right >= count || !compare(data1: array[left].getData(), data2: array[right].getData())){
                swapNode(index1: no, index2: left)
                no = left
            } else {
                swapNode(index1: no, index2: right)
                no = right
            }
            left = 2 * no + 1
            right = 2 * no + 2
        }
    }
    
    /// The function percolates up from a node of the tree to restore the max-heap property. As long as the max-heap
    /// property is corrupted, the parent and its child switch their values. We need to pay attention that, the
    /// calculated index of the parent must be a valid number. In other words, while going upper levels,we need to see
    /// that we can not go up if we are at the root of the tree.
    /// - Parameter n: Index of the starting node to restore the max-heap property.
    private func percolateUp(n: Int){
        var no : Int = n
        var parent : Int = (no - 1) / 2
        while (parent >= 0 && compare(data1: array[parent].getData(), data2: array[no].getData())){
            swapNode(index1: parent, index2: no)
            no = parent
            parent = (no - 1) / 2
        }
    }
    
    /// The function will return the first element, therefore the first element is stored in the variable, and the first
    /// element of the heap is set to the last element of the heap. After that, in order to restore the max-heap
    /// property, we percolate down the tree using the function. As a last step, the number of element in the heap is
    /// decremented by one.
    /// - Returns: The first element
    public func delete()-> T{
        let tmp = array[0]
        array[0] = array[count - 1]
        percolateDown(n: 0)
        count = count - 1
        return tmp.getData()
    }
    
    /// The insertion of a new element to the heap, proceeds from the leaf nodes to the root node. First the new element
    /// is added to the end of the heap, then as long as the max-heap property is corrupted, the new element switches
    /// place with its parent.
    /// - Parameter data: New element to be inserted.
    public func insert(data: T){
        if count <= array.count{
            array.append(HeapNode<T>(data: data))
            count = count + 1
        } else {
            count = count + 1
            array[count - 1] = HeapNode<T>(data: data)
        }
        percolateUp(n: count - 1)
    }

}

//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 16.08.2020.
//

import Foundation

public class Eigenvector : Vector{
    
    private var eigenvalue: Double
    
    /**
    A constructor of Eigenvector which takes a double eigenValue and an list values as inputs.
    It calls its super class Vector with values list and initializes eigenValue variable with its
    eigenValue input.

    - Parameters:
        - eigenvalue : eigenValue double input.
        - values : list input.
    */
    public init(eigenvalue: Double, values: [Double]){
        self.eigenvalue = eigenvalue
        super.init(values: values)
    }

    /**
    The eigenValue method which returns the eigenValue variable.

    - Returns: eigenValue variable.
    */
    public func getEigenvalue() -> Double{
        return self.eigenvalue
    }

}

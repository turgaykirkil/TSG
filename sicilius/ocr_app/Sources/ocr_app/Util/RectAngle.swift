//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 16.04.2022.
//

import Foundation

public class RectAngle{
    
    private var x: Int
    private var y: Int
    private var width: Int
    private var height: Int
    
    public init(x: Int, y: Int, width: Int, height: Int){
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    }
    
    public func contains(x: Int, y: Int) -> Bool{
        return x >= self.x && x <= self.x + width &&
        y >= self.y && y <= self.y + height
    }
    
    public func getX() -> Int{
        return x
    }
    
    public func getY() -> Int{
        return y
    }
    
    public func getWidth() -> Int{
        return width
    }
    
    public func getHeight() -> Int{
        return height
    }
}

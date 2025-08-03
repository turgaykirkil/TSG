//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 7.09.2020.
//

import Foundation

public class VectorizedDictionary: Dictionary{
    
    /**
    A constructor of VectorizedDictionary class which calls its super class Dictionary.
    */
    public init(){
        super.init(comparator: { $0.getName() < $1.getName() })
    }

    /**
    The addWord method takes a VectorizedWord as an input and adds it to the words list.

    - Parameter word : VectorizedWord input.
    */
    public func addWord(word: VectorizedWord){
        self.words.append(word)
    }

    /**
    The mostSimilarWord method takes a String name as an input, declares a maxDistance as -1 and creates a
    VectorizedWord word by getting the given name from words list. Then, it loops through the words list and if the
    current word is not equal to given input it calculates the distance between current word and given word by using
    dot product and updates the maximum distance. It then returns the result VectorizedWord which holds the most
    similar word to the given word.

    - Parameter name : String input.

    - Returns: VectorizedWord type result which holds the most similar word to the given word.
    */
    public func mostSimilarWord(name: String) -> VectorizedWord?{
        var maxDistance : Double = -1
        var result : VectorizedWord? = nil
        let word = self.getWord(name: name)
        if word == nil{
            return nil
        }
        for currentWord in self.words{
            if currentWord != word && word is VectorizedWord{
                let distance = (word as! VectorizedWord).getVector().dotProduct(v: (currentWord as! VectorizedWord).getVector())
                if distance > maxDistance{
                    maxDistance = distance
                    result = currentWord as? VectorizedWord
                }
            }
        }
        return result
    }

}

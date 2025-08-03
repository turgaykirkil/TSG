//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 7.09.2020.
//

import Foundation

public class Dictionary{
    
    var words: [Word] = []
    var filename: String = ""
    var comparator: (Word, Word) throws -> Bool

    /**
    An empty constructor of Dictionary class.
    */
    public init(comparator : @escaping (Word, Word) throws -> Bool){
        self.comparator = comparator
    }

    /**
    The getWord method takes a String name as an input and performs binary search within words list and assigns the
    result to integer variable middle. If the middle is greater than 0, it returns the item at index middle of words
    list, None otherwise.

    - Parameter name : String input.

    - Returns: the item at found index of words {@link ArrayList}, null if cannot be found.
    */
    public func getWord(name: String) -> Word?{
        let word = Word(name: name)
        let middle = self.__getPosition(word: word)
        if middle >= 0{
            return self.words[middle]
        }
        return nil
    }

    /**
    The getWordIndex method takes a String name as an input and performs binary search within words list and assigns
    the result to integer variable middle. If the middle is greater than 0, it returns the index middle, -1
    otherwise.

    - Parameter name : String input.

    - Returns: found index of words list, -1 if cannot be found.
    */
    public func getWordIndex(name: String) -> Int{
        let word = Word(name: name)
        let middle = self.__getPosition(word: word)
        if middle >= 0{
            return middle
        }
        return -1
    }

    /**
    RemoveWord removes a word with the given name

    - Parameter name : Name of the word to be removed.
    */
    public func removeWord(name: String){
        let index = self.getWordIndex(name: name)
        if index != -1{
            self.words.remove(at: index)
        }
    }

    /**
    The size method returns the size of the words list.

    - Returns: The size of the words list.
    */
    public func size() -> Int{
        return self.words.count
    }

    /**
    The getWordWithIndex method which takes an index as an input and returns the value at given index of words list.

    - Parameter index : index to get the value.

    - Returns: The value at given index of words list.
    */
    public func getWordWithIndex(index: Int) -> Word{
        return self.words[index]
    }

    /**
    The longestWordSize method loops through the words list and returns the item with the maximum word length.

    - Returns: The item with the maximum word length.
    */
    public func longestWordSize() -> Int{
        var maxLength : Int = 0
        for word in self.words{
            if word.getName().count > maxLength{
                maxLength = word.getName().count
            }
        }
        return maxLength
    }
    
    /// Checks if a given word exists in the dictionary by performing a binary search on the words array.
    /// - Parameter word: Searched word
    /// - Returns: the index of the search word, if it is contained in the words array; otherwise, (-(insertion point) - 1). The
    /// insertion point is defined as the point at which the word would be inserted into the words array.
    public func __getPosition(word: Word) -> Int{
        var lo : Int = 0
        var hi : Int = self.words.count - 1
        while lo <= hi{
            let mid = (lo + hi) / 2
            if self.words[mid].getName() == word.getName(){
                return mid
            }
            do{
                if try self.comparator(self.words[mid], word){
                    lo = mid + 1
                } else {
                    hi = mid - 1
                }
            } catch {
            }
        }
        return -(lo + 1)
    }

    /**
    The getWordStartingWith method takes a String hash as an input and performs binary search within words list and
    assigns the result to integer variable middle. If the middle is greater than 0, it returns the index middle,
    -middle-1 otherwise.

    PARAMETERS
    ----------
    _hash : String
        String input.

    RETURNS
    -------
    Int
        Found index of words list, -middle-1 if cannot be found.
    */
    public func getWordStartingWith(_hash: String) -> Int{
        let word = Word(name: _hash)
        let middle = self.__getPosition(word: word)
        if middle < 0{
            return -middle - 1
        } else {
            return middle
        }
    }
}

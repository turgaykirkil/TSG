//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 5.09.2020.
//

import Foundation

public class TrieNode{
    
    private var __children: [Character: TrieNode] = [:]
    private var __words: Set<Word> = []
    
    /**
    A constructor of TrieNode class which creates a new children.
    */
    public init(){
    }
    
    /**
    The addWord method takes a String word, an index, and a Word root as inputs. First it creates a TrieNode child
    and it directly adds it to the set when the given index is equal to the length of given word.

    Then, it extracts the character at given index of given word and if children dictionary contains a mapping for
    the extracted character, it assigns it to the TrieNode child, else it creates a new TrieNode and assigns it to
    the child. At the end, it recursively calls the addWord method with the next index of child and puts the
    character with the child into the children dictionary.

    - Parameters:
        - word : String input.
        - index : Integer index.
        - root : Word input to add.
    */
    public func addWord(word: String, root: Word, index: Int = 0){
        if index == word.count{
            self.__words.insert(root)
            return
        }
        let ch = Word.charAt(s: word, i: index)
        var child: TrieNode
        if self.__children[ch] != nil{
            child = self.__children[ch]!
        } else {
            child = TrieNode()
        }
        child.addWord(word: word, root: root, index: index + 1)
        self.__children[ch] = child
    }

    /**
    The getChild method takes a character and gets its corresponding value from children dictionary.

    - Parameter ch : Character input.

    - Returns: the value from children dictionary.
    */
    public func getChild(ch: Character) -> TrieNode?{
        return self.__children[ch]
    }

    /**
    The getWords method returns the words set.

    - Returns: the words set.
    */
    public func getWords() -> Set<Word>{
        return self.__words
    }
    
}

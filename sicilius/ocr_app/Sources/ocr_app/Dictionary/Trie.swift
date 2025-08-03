//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 5.09.2020.
//

import Foundation

public class Trie{
    
    private var __rootNode: TrieNode
    
    /**
    A constructor of Trie class which creates a new TrieNode as rootNode.
    */
    public init(){
        self.__rootNode = TrieNode()
    }

    /**
    The addWord method which takes a String word and a Word root as inputs and adds given word and root to the
    rootNode.

    - Parameters:
        - word : String input.
        - root : Word input.
    */
    public func addWord(word: String, root: Word){
        self.__rootNode.addWord(word: word, root: root)
    }

    /**
    The getWordsWithPrefix method which takes a String surfaceForm as an input. First it creates a TrieNode current
    and assigns the rootNode to it, then it creates a new set words. It loops i times where i ranges from 0 to
    length of surfaceForm and assigns current's child that corresponds to the surfaceForm's char at index i and
    assigns it as TrieNode current. If current is not None, it adds all words of current to the words set.

    - Parameter surfaceForm : String input.

    - Returns: words set.
    */
    public func getWordsWithPrefix(surfaceForm: String) -> Set<Word>{
        var current : TrieNode = self.__rootNode
        var words : Set<Word> = []
        for i in 0..<surfaceForm.count{
            let currentNew = current.getChild(ch: surfaceForm[surfaceForm.index(surfaceForm.startIndex, offsetBy: i)])
            if currentNew != nil{
                current = currentNew!
                words.formUnion(current.getWords())
            } else {
                break
            }
        }
        return words
    }

    /**
    The getCompoundWordStartingWith method takes a String hash. First it creates a TrieNode current and assigns
    the rootNode to it. Then it loops i times where i ranges from 0 to length of given hash and assigns current's
    child that corresponds to the hash's char at index i and assigns it as current. If current is None, it returns
    null.

    If current is not None, it loops through the words of current TrieNode and if it is a Portmanteau word, it
    directly returns the word.

    - Parameter _hash : String input.

    - Returns: nil if TrieNode is None, otherwise portmanteau word.
    */
    public func getCompoundWordStartingWith(_hash: String) -> TxtWord?{
        var current : TrieNode? = self.__rootNode
        for i in 0..<_hash.count{
            current = current!.getChild(ch: Word.charAt(s: _hash, i: i))
            if current == nil{
                return nil
            }
        }
        if current != nil{
            for word in current!.getWords(){
                if (word as! TxtWord).isPortmanteau(){
                    return word as? TxtWord
                }
            }
        }
        return nil
    }
}

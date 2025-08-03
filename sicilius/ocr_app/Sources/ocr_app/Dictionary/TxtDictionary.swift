//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 7.09.2020.
//

import Foundation

public class TxtDictionary: Dictionary{
    
    private var __misspelledWords : [String: String]
    
    /// Empty constructor of TxtDictionary class. Sets the WordComparator to TurkishWordComparator, loads the
    /// default Turkish dictionary, Turkish misspellings file and Turkish morphological lexicon, which contains the
    /// subword units to Turkish root words.
    public init(){
        self.__misspelledWords = [:]
        super.init(comparator: { $0.getName().compare($1.getName(), locale: Locale(identifier: "tr")) == .orderedAscending || $0.getName().compare($1.getName(), locale: Locale(identifier: "tr")) == .orderedSame})
        self.filename = "turkish_dictionary"
        self.__loadFromText()
        self.__loadMisspelledWords()
        self.__loadMorphologicalLexicon()
    }
    
    /// Another constructor of {@link TxtDictionary} class which takes a String filename as input.
    /// And calls its super class Dictionary assigns given filename input to the
    /// filename variable. Then, it calls loadFromText method with given filename.
    /// - Parameter fileName: String input.
    public init(fileName: String){
        self.__misspelledWords = [:]
        super.init(comparator: { $0.getName().compare($1.getName(), locale: Locale(identifier: "tr")) == .orderedAscending || $0.getName().compare($1.getName(), locale: Locale(identifier: "tr")) == .orderedSame})
        self.filename = fileName
        self.__loadFromText(fileName: self.filename)
        self.__loadMorphologicalLexicon()
    }

    /**
    Constructor of TxtDictionary class which takes a String filename as input. And calls its super class
    Dictionary, assigns given filename input to the filename variable. Then, it calls loadFromText method with given
    filename.

    - Parameter fileName : String input.
    */
    public init(fileName: String, misspelledFileName: String, comparator: @escaping (Word, Word) throws -> Bool){
        self.__misspelledWords = [:]
        super.init(comparator: comparator)
        self.filename = fileName
        self.__loadFromText(fileName: self.filename)
        self.__loadMisspelledWords(fileName: misspelledFileName)
        self.__loadMorphologicalLexicon()
    }

    /**
    The addPerson method takes a String name and calls addWithFlag method with given name and IS_AD flag.

    - Parameter name : String input.
    */
    public func addPerson(name: String){
        _ = self.addWithFlag(name: name, flag: "IS_AD")
    }

    /**
    The addNumber method takes a String name and calls addWithFlag method with given name and IS_SAYI flag.

    - Parameter name : String input.
    */
    public func addNumber(name: String){
        _ = self.addWithFlag(name: name, flag: "IS_SAYI")
    }

    /**
    The addRealNumber method takes a String name and calls addWithFlag method with given name and IS_REELSAYI flag.

    - Parameter name : String input.
    */
    public func addRealNumber(name: String){
        _ = self.addWithFlag(name: name, flag: "IS_REELSAYI")
    }

    /**
    The addFraction method takes a String name and calls addWithFlag method with given name and IS_KESIR flag.

    - Parameter name : String input.
    */
    public func addFraction(name: String){
        _ = self.addWithFlag(name: name, flag: "IS_KESIR")
    }

    /**
    The addTime method takes a String name and calls addWithFlag method with given name and IS_ZAMAN flag.

    - Parameter name : String input.
    */
    public func addTime(name: String){
        _ = self.addWithFlag(name: name, flag: "IS_ZAMAN")
    }

    /**
    The addDate method takes a String name and calls addWithFlag method with given name and IS_TARIH flag.

    - Parameter name : String input.
    */
    public func addDate(name: String){
        _ = self.addWithFlag(name: name, flag: "IS_TARIH")
    }

    /**
    The addPercentage method takes a String name and calls addWithFlag method with given name and IS_YUZDE flag.

    - Parameter name : String input.
    */
    public func addPercentage(name: String){
        _ = self.addWithFlag(name: name, flag: "IS_YUZDE")
    }

    /**
    The addOrganization method takes a String name and calls addWithFlag method with given name and IS_KURUM flag.

    - Parameter name : String input.
    */
    public func addOrganization(name: String){
        _ = self.addWithFlag(name: name, flag: "IS_KURUM")
    }

    /**
    The addProperNoun method takes a String name and calls addWithFlag method with given name and IS_OZEL flag.

    - Parameter name : String input.

    - Returns: true if given name is in words list, false otherwise.
    */
    public func addProperNoun(name: String) -> Bool{
        return self.addWithFlag(name: name, flag: "IS_OZEL")
    }

    /**
    The addNoun method takes a String name and calls addWithFlag method with given name and IS_ISIM flag.

    - Parameter name : String input.

    - Returns: true if given name is in words list, false otherwise.
    */
    public func addNoun(name: String) -> Bool{
        return self.addWithFlag(name: name, flag: "IS_ISIM")
    }

    /**
    The addVerb method takes a String name and calls addWithFlag method with given name and IS_FIIL flag.

    - Parameter name : String input.

    - Returns: true if given name is in words list, false otherwise.
    */
    public func addVerb(name: String) -> Bool{
        return self.addWithFlag(name: name, flag: "IS_FIIL")
    }

    /**
    The addAdjective method takes a String name and calls addWithFlag method with given name and IS_ADJ flag.

    - Parameter name : String input.

    - Returns: true if given name is in words list, false otherwise.
    */
    public func addAdjective(name: String) -> Bool{
        return self.addWithFlag(name: name, flag: "IS_ADJ")
    }

    /**
    The addAdverb method takes a String name and calls addWithFlag method with given name and IS_ADV flag.

    - Parameter name : String input.

    - Returns: true if given name is in words list, false otherwise.
    */
    public func addAdverb(name: String) -> Bool{
        return self.addWithFlag(name: name, flag: "IS_ADV")
    }

    /**
    The addPronoun method takes a String name and calls addWithFlag method with given name and IS_ZAMIR flag.

    - Parameter name : String input.

    - Returns: true if given name is in words list, false otherwise.
    */
    public func addPronoun(name: String) -> Bool{
        return self.addWithFlag(name: name, flag: "IS_ZAMIR")
    }

    /**
    The addHeader method takes a String name and calls addWithFlag method with given name and IS_HEADER flag.

    - Parameter name : String input.

    - Returns: true if given name is in words list, false otherwise.
    */
    public func addHeader(name: String) -> Bool{
        return self.addWithFlag(name: name, flag: "IS_HEADER")
    }

    /**
    The addWithFlag method takes a String name and a flag as inputs. First it creates a TxtWord word, then if
    given name is not in words list it creates new TxtWord with given name and assigns it to
    the word and adds given flag to the word, it also add newly created word to the words list's index
    found by performing a binary search and return true at the end. If given name is in words list,
    it adds it the given flag to the word.

    - Parameters:
        - name : String input.
        - flag : String flag.

    - Returns: true if given name is in words list, false otherwise.
    */
    public func addWithFlag(name: String, flag: String) -> Bool{
        if self.getWord(name: name.lowercased()) == nil{
            let word = TxtWord(name: name.lowercased())
            word.addFlag(flag: flag)
            let middle = self.__getPosition(word: word)
            self.words.insert(word, at: -middle - 1)
            return true
        } else {
            let word = self.getWord(name: name.lowercased())
            if word is TxtWord && !(word as! TxtWord).containsFlag(flag: flag){
                (word as! TxtWord).addFlag(flag: flag)
            }
        }
        return false
    }
    
    /**
    The loadFromText method takes a String filename as an input. It reads given file line by line and splits
    according to space and assigns each word to the String array. Then, adds these word with their flags to the
    words list. At the end it sorts the words list.

    - Parameter fileName : File name input.
    */
    public func __loadFromText(fileName: String = "turkish_dictionary"){
        let url = Bundle.module.url(forResource: fileName, withExtension: "txt")
        do{
            let fileContent = try String(contentsOf: url!, encoding: .utf8)
            let lines : [String] = fileContent.split { $0.isNewline }.map(String.init)
            for line in lines{
                let wordList : [String] = line.split(separator: " ").map(String.init)
                if wordList.count > 0{
                    let currentWord = TxtWord(name: wordList[0])
                    for i in 1..<wordList.count{
                        currentWord.addFlag(flag: wordList[i])
                    }
                    self.words.append(currentWord)
                }
            }
            try self.words.sort(by: comparator)
        }catch{
        }
    }

    /**
    The loadMisspellWords method takes a String filename as an input. It reads given file line by line and splits
    according to space and assigns each word with its misspelled form to the the misspelledWords hashMap.

    - Parameter fileName : File name input.
    */
    public func __loadMisspelledWords(fileName: String = "turkish_misspellings"){
        let url = Bundle.module.url(forResource: fileName, withExtension: "txt")
        do{
            let fileContent = try String(contentsOf: url!, encoding: .utf8)
            let lines : [String] = fileContent.split { $0.isNewline }.map(String.init)
            for line in lines{
                let wordList : [String] = line.split(separator: " ").map(String.init)
                if wordList.count == 2{
                    self.__misspelledWords[wordList[0]] = wordList[1]
                }
            }
        }catch{
        }
    }
    
    /// Loads the morphological lexicon of a given language. Only Turkish is currently supported. Morphological lexicon
    /// contains subwords (possibly meaningful words or metamorphemes) of each root word in the Turkish dictionary. For
    /// example, abacılık has subwords aba+CH+LHK.
    /// - Parameter fileName: Morphological lexicon file
    public func __loadMorphologicalLexicon(fileName: String = "turkish_morphological_lexicon"){
        let url = Bundle.module.url(forResource: fileName, withExtension: "txt")
        do{
            let fileContent = try String(contentsOf: url!, encoding: .utf8)
            let lines : [String] = fileContent.split { $0.isNewline }.map(String.init)
            for line in lines{
                let wordList : [String] = line.split(separator: " ").map(String.init)
                if wordList.count == 2{
                    let word = self.getWord(name: wordList[0])
                    if word != nil{
                        let txtWord = word as! TxtWord
                        txtWord.setMorphology(morphology: wordList[1])
                    }
                }
            }
        }catch{
        }
    }

    /**
    The getCorrectForm returns the correct form of a misspelled word.

    - Parameter misspelledWord : Misspelled form.

    - Returns: Correct form.
    */
    public func getCorrectForm(misspelledWord: String) -> String{
        if self.__misspelledWords[misspelledWord] != nil{
            return self.__misspelledWords[misspelledWord]!
        }
        return ""
    }

    /**
    The addWordWhenRootSoften is used to add word to Trie whose last consonant will be soften.
    For instance, in the case of Dative Case Suffix, the word is 'müzik' when '-e' is added to the word, the last
    char is drooped and root became 'müzi' and by changing 'k' into 'ğ' the word transformed into 'müziğe' as in the
    example of 'Herkes müziğe doğru geldi'.

    In the case of accusative, possessive of third person and a derivative suffix, the word is 'kanat' when '-i' is
    added to word, last char is dropped, root became 'kana' then 't' transformed into 'd' and added to Trie. The
    word is changed into 'kanadı' as in the case of 'Kuşun kırık kanadı'.

    - Parameters:
        - trie : the name of the Trie to add the word.
        - last : the last char of the word to be soften.
        - root : the substring of the word whose last one or two chars are omitted from the word to bo softed.
        - word : the original word.
    */
    public func __addWordWhenRootSoften(trie: Trie, last: Character, root: String, word: TxtWord){
        if last == "p"{
            trie.addWord(word: root + "b", root: word)
        } else if last == "ç"{
            trie.addWord(word: root + "c", root: word)
        } else if last == "t"{
            trie.addWord(word: root + "d", root: word)
        } else if last == "k" || last == "g"{
            trie.addWord(word: root + "ğ", root: word)
        }
    }

    /**
    The prepareTrie method is used to create a Trie with the given dictionary. First, it gets the word from
    dictionary, then checks some exceptions like 'ben' which does not fit in the consonant softening rule and
    transforms into 'bana', and later on it generates a root by removing the last char from the word however if the
    length of the word is greater than 1, it also generates the root by removing the last two chars from the word.

    Then, it gets the last char of the root and adds root and word to the result Trie. There are also special cases
    such as;
    lastIdropsDuringSuffixation condition, if it is true then addWordWhenRootSoften method will be used rather than
    addWord.
    Ex : metin + i = metni
    isPortmanteauEndingWithSI condition, if it is true then addWord method with rootWithoutLastTwo will be used.
    Ex : ademelması + lar = ademelmaları
    isPortmanteau condition, if it is true then addWord method with rootWithoutLast will be used.
    Ex : mısıryağı + lar = mısıryağları
    vowelEChangesToIDuringYSuffixation condition, if it is then addWord method with rootWithoutLast will be used
    depending on the last char whether it is 'e' or 'a'.
    Ex : ye + iniz - yiyiniz
    endingKChangesIntoG condition, if it is true then addWord method with rootWithoutLast will be used with added
    'g'.
    Ex : ahenk + i = ahengi

    - Returns: the resulting Trie.
    */
    public func prepareTrie() -> Trie{
        let result : Trie = Trie()
        var lastBefore : Character = " "
        for i in 0..<self.size(){
            let word = self.getWordWithIndex(index: i)
            if word is TxtWord{
                let root = word.getName()
                let length = root.count
                if root == "ben"{
                    result.addWord(word: "bana", root: word)
                }
                if root == "sen"{
                    result.addWord(word: "sana", root: word)
                }
                let rootWithoutLast : String = String(root[..<root.index(root.startIndex, offsetBy: length - 1)])
                var rootWithoutLastTwo : String
                if length > 1{
                    rootWithoutLastTwo = String(root[..<root.index(root.startIndex, offsetBy: length - 2)])
                } else {
                    rootWithoutLastTwo = ""
                }
                if length > 1{
                    lastBefore = Word.charAt(s: root, i: length - 2)
                }
                var last : Character
                last = Word.charAt(s: root, i: length - 1)
                result.addWord(word: root, root: word)
                if (word as! TxtWord).lastIdropsDuringSuffixation() || (word as! TxtWord).lastIdropsDuringPassiveSuffixation(){
                    if (word as! TxtWord).rootSoftenDuringSuffixation(){
                        self.__addWordWhenRootSoften(trie: result, last: last, root: rootWithoutLastTwo, word: word as! TxtWord)
                    } else{
                        result.addWord(word: String(rootWithoutLastTwo) + String(last), root: word)
                    }
                }
                if (word as! TxtWord).isPortmanteauEndingWithSI(){
                    result.addWord(word: rootWithoutLastTwo, root: word)
                }
                if (word as! TxtWord).rootSoftenDuringSuffixation(){
                    self.__addWordWhenRootSoften(trie: result, last: last, root: rootWithoutLast, word: word as! TxtWord)
                }
                if (word as! TxtWord).isPortmanteau(){
                    if (word as! TxtWord).isPortmanteauFacedVowelEllipsis(){
                        result.addWord(word: rootWithoutLastTwo + String(last) + String(lastBefore), root: word)
                    } else {
                        if (word as! TxtWord).isPortmanteauFacedSoftening(){
                            if lastBefore == "b"{
                                result.addWord(word: rootWithoutLastTwo + "p", root: word)
                            } else if lastBefore == "c"{
                                result.addWord(word: rootWithoutLastTwo + "ç", root: word)
                            } else if lastBefore == "d"{
                                result.addWord(word: rootWithoutLastTwo + "t", root: word)
                            } else if lastBefore == "ğ"{
                                result.addWord(word: rootWithoutLastTwo + "k", root: word)
                            }
                        } else {
                            result.addWord(word: rootWithoutLast, root: word)
                        }
                    }
                }
                if (word as! TxtWord).vowelEChangesToIDuringYSuffixation() || (word as! TxtWord).vowelAChangesToIDuringYSuffixation(){
                    if last == "e"{
                        result.addWord(word: rootWithoutLast, root: word)
                    } else if last == "a"{
                        result.addWord(word: rootWithoutLast, root: word)
                    }
                }
                if (word as! TxtWord).endingKChangesIntoG(){
                    result.addWord(word: rootWithoutLast + "g", root: word)
                }
            }
        }
        return result
    }

}

//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 6.09.2020.
//

import Foundation

public class SyllableList{
    
    private var __syllables: [Syllable]

    /**
     A constructor of SyllableList class which takes a String word as an input. First it creates a syllable
     list and a sbSyllable. Then it loops i times, where i ranges from 0 to length of given word, first
     it gets the ith character of given word and checks whether it is a vowel and the last character of the word.

     If it is a vowel it appends it to the sbSyllable and if it is the last vowel it also appends the next character
     to the sbSyllable. Then, it adds the sbSyllable to the syllables list.

     If it is not a vowel, and the sbSyllable's length is 1 also the previous character is a consonant it gets the
     last item of syllables list since there cannot be a Turkish word which starts with two consonants. However, if
     it is two last characters of word, then it adds it to the syllablelist. At the end, it updates the syllables
     list.

     - Parameter word : String input.
    */
    public init(word: String){
        self.__syllables = []
        var sbSyllable : String = ""
        var i : Int = 0
        while i < word.count{
            let c : Character = Word.charAt(s: word, i: i)
            let isVowel = TurkishLanguage.isVowel(ch: c)
            let isLastChar = (i == word.count - 1)
            if isVowel{
                sbSyllable += String(c)
                if i == word.count - 2{
                    sbSyllable += String(Word.charAt(s: word, i: i + 1))
                    i = i + 1
                }
                self.__syllables.append(Syllable(syllable: sbSyllable))
                sbSyllable = ""
            } else {
                let tempSyl : String = sbSyllable
                if tempSyl.count == 1{
                    if !TurkishLanguage.isVowel(ch: Word.charAt(s: tempSyl, i: 0)){
                        if self.__syllables.count == 0{
                            sbSyllable += String(c)
                            i = i + 1
                            continue
                        }
                        let lastPos = self.__syllables.count - 1
                        var string : String = self.__syllables[lastPos].getText()
                        string = string + tempSyl
                        if isLastChar{
                            string = string + String(c)
                        }
                        self.__syllables[lastPos] = Syllable(syllable: string)
                        sbSyllable = ""
                    }
                }
                sbSyllable += String(c)
            }
            i = i + 1
        }
    }

    /**
    The getSyllables method creates a new list syllables and loops through the globally defined syllables
    list and adds each item to the newly created syllables list.

    - Returns: list syllables.
    */
    public func getSyllables() -> [String]{
        var syllables : [String] = []
        for syllable in self.__syllables{
            syllables.append(syllable.getText())
        }
        return syllables
    }

}

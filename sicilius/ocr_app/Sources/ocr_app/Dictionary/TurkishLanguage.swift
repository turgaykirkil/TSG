//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 6.09.2020.
//

import Foundation

public class TurkishLanguage: Language{
    
    public static let VOWELS = "aeıioöuüâî"
    public static let BACK_VOWELS = "aıouâ"
    public static let FRONT_VOWELS = "eiöüî"
    public static let BACK_ROUNDED_VOWELS = "ou"
    public static let BACK_UNROUNDED_VOWELS = "aıâ"
    public static let FRONT_ROUNDED_VOWELS = "öü"
    public static let FRONT_UNROUNDED_VOWELS = "eiî"
    public static let CONSONANT_DROPS = "nsy"
    public static let CONSONANTS = "bcçdfgğhjklmnprsştvyzxqw"
    public static let SERT_SESSIZ = "çfhkpsşt"
    public static let LOWERCASE_LETTERS = "abcçdefgğhıijklmnoöprsştuüvyz"
    public static let UPPERCASE_LETTERS = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    public static let LETTERS = LOWERCASE_LETTERS + UPPERCASE_LETTERS

    /**
    The isVowel method takes a character as an input and returns true if given character is a vowel.

    - Parameter ch : Character input to check.

    - Returns: true if given character is a vowel.
    */
    public static func isVowel(ch: Character) -> Bool{
        return VOWELS.contains(ch)
    }

    /**
    The isBackVowel method takes a character as an input and returns true if given character is a back vowel.

    - Parameter ch : Character input to check.

    - Returns: true if given character is a back vowel.
    */
    public static func isBackVowel(ch: Character) -> Bool{
        return BACK_VOWELS.contains(ch)
    }

    /**
    The isFrontVowel method takes a character as an input and returns true if given character is a front vowel.

    - Parameter ch : Character input to check.

    - Returns: true if given character is a front vowel.
    */
    public static func isFrontVowel(ch: Character) -> Bool{
        return FRONT_VOWELS.contains(ch)
    }

    /**
    The isBackRoundedVowel method takes a character as an input and returns true if given character is a back
    rounded vowel.

    - Parameter ch : Character input to check.

    - Returns: true if given character is a back rounded vowel.
    */
    public static func isBackRoundedVowel(ch: Character) -> Bool{
        return BACK_ROUNDED_VOWELS.contains(ch)
    }

    /**
    The isFrontRoundedVowel method takes a character as an input and returns true if given character is a front
    rounded vowel.

    - Parameter ch : Character input to check.

    - Returns: true if given character is a front rounded vowel.
    */
    public static func isFrontRoundedVowel(ch: Character) -> Bool{
        return FRONT_ROUNDED_VOWELS.contains(ch)
    }

    /**
    The isBackUnroundedVowel method takes a character as an input and returns true if given character is a back
    unrounded vowel.

    - Parameter ch : Character input to check.

    - Returns: true if given character is a back unrounded vowel.
    */
    public static func isBackUnroundedVowel(ch: Character) -> Bool{
        return BACK_UNROUNDED_VOWELS.contains(ch)
    }

    /**
    The isFrontUnroundedVowel method takes a character as an input and returns true if given character is a front
    unrounded vowel.

    - Parameter ch : Character input to check.

    - Returns: true if given character is a front unrounded vowel.
    */
    public static func isFrontUnroundedVowel(ch: Character) -> Bool{
        return FRONT_UNROUNDED_VOWELS.contains(ch)
    }

    /**
    The isConsonantDrop method takes a character as an input and returns true if given character is a dropping
    consonant

    - Parameter ch : Character input to check.

    - Returns: true if given character is a dropping consonant.
    */
    public static func isConsonantDrop(ch: Character) -> Bool{
        return CONSONANT_DROPS.contains(ch)
    }

    /**
    The isConsonant method takes a character as an input and returns true if given character is a consonant

    - Parameter ch : Character input to check.

    - Returns: true if given character is a consonant.
    */
    public static func isConsonant(ch: Character) -> Bool{
        return CONSONANTS.contains(ch)
    }

    /**
    The isSertSessiz method takes a character as an input and returns true if given character is a sert sessiz

    - Parameter ch : Character input to check.

    - Returns: true if given character is a sert sessiz.
    */
    public static func isSertSessiz(ch: Character) -> Bool{
        return SERT_SESSIZ.contains(ch)
    }

}

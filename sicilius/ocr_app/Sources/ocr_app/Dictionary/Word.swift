//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 5.09.2020.
//

import Foundation

open class Word : Comparable, Equatable, Hashable{
    
    private var name: String

    /**
    A constructor of Word class which gets a String name as an input and assigns to the name variable.

    - Parameter name : String input.
    */
    public init(name: String){
        self.name = name
    }

    public static func < (lhs: Word, rhs: Word) -> Bool {
        return lhs.name < rhs.name
    }

    public static func == (lhs: Word, rhs: Word) -> Bool {
        return lhs.name == rhs.name
    }

    public func hash(into hasher: inout Hasher) {
        hasher.combine(name)
    }
    
    /**
    The overridden __str__ method returns the name variable.

    RETURNS
    -------
    String
        the name variable.
    */
    open func description() -> String{
        return self.name
    }

    /**
    The charCount method returns the length of name variable.

    - Returns: the length of name variable.
    */
    public func charCount() -> Int{
        return self.name.count
    }

    /**
    Getter for the name variable.

    - Returns: name variable.
    */
    public func getName() -> String{
        return self.name
    }

    /**
    Setter for the name variable.

    - Parameters name : String input.
    */
    public func setName(name: String){
        self.name = name
    }
    
    /// Returns the UTF8 character value at the specified index of an input string
    /// - Parameters:
    ///   - s: Input string
    ///   - i: The index of the character
    /// - Returns: UTF8 character value at the specified index
    public static func charAt(s: String, i: Int) -> Character{
        return s[s.index(s.startIndex, offsetBy: i)];
    }
    
    /// Returns a substring until the first occurence of the given character
    /// - Parameters:
    ///   - s: Input string
    ///   - ch: Character until which the substring is formed.
    /// - Returns: Substring until the first occurrence of the given character
    public static func substringUntil(s: String, ch: String) -> String{
        return String(s[..<s.range(of: ch)!.lowerBound])
    }
    
    /// Returns a substring from the first occurrence of the given character
    /// - Parameters:
    ///   - s: Input string
    ///   - ch: Character from which the substring is returned
    /// - Returns: Substring from the first occurrence of the given character
    public static func substringFrom(s: String, ch: String) -> String{
        return String(s[s.range(of: ch)!.upperBound...])
    }
    
    /// Converts the given string into its capital form
    /// - Parameter s: Given string which will be converted to its capital form
    /// - Returns: Capitalized form of the input string.
    public static func toCapital(s: String) -> String{
        var result : String = Word.uppercase(s: String(Word.charAt(s: s, i: 0)))
        for i in 1..<s.count{
            result += String(Word.charAt(s: s, i: i))
        }
        return result
    }

    /// Returns an uppercase copy of the given input string
    /// - Parameter s: Input string
    /// - Returns: Uppercase copy of the input string
    public static func uppercase(s: String) -> String{
        var result : String = ""
        for i in 0..<s.count{
            switch charAt(s: s, i: i) {
                case "ç":
                    result += "Ç"
                case "ö":
                    result += "Ö"
                case "ğ":
                    result += "Ğ"
                case "ü":
                    result += "Ü"
                case "ş":
                    result += "Ş"
                case "ı":
                    result += "I"
                case "i":
                    result += "İ"
                default:
                    result += charAt(s: s, i: i).uppercased()
            }
        }
        return result
    }
    
    /// Returns a lowercase copy of the given input string
    /// - Parameter s: Input string
    /// - Returns: Lowercase copy of the input string
    public static func lowercase(s: String) -> String{
        var result : String = ""
        for i in 0..<s.count{
            switch charAt(s: s, i: i) {
                case "Ç":
                    result += "ç"
                case "Ö":
                    result += "ö"
                case "Ğ":
                    result += "ğ"
                case "Ü":
                    result += "ü"
                case "Ş":
                    result += "ş"
                case "I":
                    result += "ı"
                case "İ":
                    result += "i"
                default:
                    result += charAt(s: s, i: i).lowercased()
            }
        }
        return result
    }

    /**
     * The beforeLastVowel method takes a {@link String} stem as an input. It loops through the given stem and returns
     * the second last vowel.
        - Parameters:
            - stem: String input.
        - Returns: Vowel before the last vowel.
     */
    public static func beforeLastVowel(stem: String) -> Character{
        var before : Int = 1
        var last : Character = "0"
        var i : Int = stem.count - 1
        while i >= 0 {
            if TurkishLanguage.isVowel(ch: Word.charAt(s: stem, i: i)) {
                if (before == 1) {
                    last = Word.charAt(s: stem, i: i)
                    before -= 1
                    i -= 1
                    continue
                }
                return Word.charAt(s: stem, i: i)
            }
            i -= 1
        }
        return last
    }
    
    /**
     * The lastVowel method takes a {@link String} stem as an input. It loops through the given stem and returns
     * the last vowel.
        - Parameters:
            - stem: String input.
        - Returns: the last vowel.
     */
    public static func lastVowel(stem: String) -> Character{
        var i : Int = stem.count - 1
        while i >= 0 {
            if TurkishLanguage.isVowel(ch: Word.charAt(s: stem, i: i)) {
                return Word.charAt(s: stem, i: i)
            }
            i -= 1
        }
        i = stem.count - 1
        while i >= 0 {
            if Word.charAt(s: stem, i: i) >= "0" && Word.charAt(s: stem, i: i) <= "9" {
                return Word.charAt(s: stem, i: i)
            }
            i -= 1
        }
        return "0"
    }
    
    /**
     * The lastPhoneme method takes a {@link String} stem as an input. It then returns the last phoneme of the given stem.
        - Parameters:
            - stem: String input.
        - Returns: the last phoneme.
     */
    public static func lastPhoneme(stem: String) -> Character{
        if stem.count == 0 {
            return " ";
        }
        if Word.charAt(s: stem, i: stem.count - 1) != "'" {
            return Word.charAt(s: stem, i: stem.count - 1)
        } else {
            return Word.charAt(s: stem, i: stem.count - 2)
        }
    }
    

    /**
    The isCapital method takes a String surfaceForm as an input and returns true if the character at first index of
    surfaceForm is a capital letter, false otherwise.

    - Parameter surfaceForm : String input to check the first character.

    - Returns: true if the character at first index of surfaceForm is a capital letter, false otherwise.
    */
    public static func isCapital(surfaceForm: String) -> Bool{
        return TurkishLanguage.UPPERCASE_LETTERS.contains(charAt(s: surfaceForm, i: 0))
    }

    /**
    The isPunctuationSymbol method takes a String surfaceForm as an input and returns true if it is a punctuation,
    False otherwise.
    Grave accent : \u0060
    Left quotation mark : \u201C
    Right quotation mark : \u201D
    Left single quotation mark : \u2018
    Horizontal ellipsis : \u2026

    - Parameter surfaceForm : String input to check.

    - Returns: true if it is a punctuation, false otherwise.
    */
    public static func isPunctuationSymbol(surfaceForm: String) -> Bool{
        return surfaceForm == "." || surfaceForm == "..." || surfaceForm == "[" || surfaceForm == "]" ||
               surfaceForm == "\u{2026}" || surfaceForm == "%" || surfaceForm == "&" || surfaceForm == "=" ||
               surfaceForm == "\u{0060}\u{0060}" || surfaceForm == "\u{0060}" || surfaceForm == "''" || surfaceForm == "$" ||
               surfaceForm == "!" || surfaceForm == "?" || surfaceForm == "," || surfaceForm == ":" ||
               surfaceForm == "--" || surfaceForm == ";" || surfaceForm == "(" || surfaceForm == ")" ||
               surfaceForm == "'" || surfaceForm == "\"" || surfaceForm == "\u{201C}" || surfaceForm == "\u{2018}" ||
               surfaceForm == "\u{201D}" || surfaceForm == "…" || surfaceForm == "\u{25CF}" || surfaceForm == "/" ||
               surfaceForm == "-" || surfaceForm == "+" || surfaceForm == "-LRB-" || surfaceForm == "-RRB-" ||
               surfaceForm == "-LCB-" || surfaceForm == "-RCB-" || surfaceForm == "-LSB-" || surfaceForm == "-RSB-"
    }

    /**
    The isHonorific method takes a String surfaceForm as an input and after converting it to lower case it returns
    true if it equals to "bay" || "bayan", false otherwise.

    - Parameter surfaceForm : String input to check.

    - Returns: true if it equals to "bay" || "bayan", false otherwise.
    */
    public static func isHonorific(surfaceForm: String) -> Bool{
        let lowerCase = surfaceForm.lowercased()
        return lowerCase == "bay" || lowerCase == "bayan"
    }

    /**
    The isOrganization method takes a String surfaceForm as an input and after converting it to lower case it
    returns true if it equals to "corp", "inc.", || "co.", and false otherwise.

    - Parameter surfaceForm : String input to check.

    - Returns: true if it equals to "corp", "inc.", || "co.", and false otherwise.
    */
    public static func isOrganization(surfaceForm: String) -> Bool{
        let lowerCase = surfaceForm.lowercased()
        return lowerCase == "corp" || lowerCase == "inc." || lowerCase == "co."
    }

    /**
    The isMoney method takes a String surfaceForm as an input and after converting it to lower case it returns true
    if it equals to one of the dolar, sterlin, paunt, ons, ruble, mark, frank, yan, sent, yen' || $, and false
    otherwise.

    - Parameter surfaceForm : String input to check.

    - Returns: true if it equals to one of the dolar, sterlin, paunt, ons, ruble, mark, frank, yan, sent, yen' || $, and
        false otherwise.
    */
    public static func isMoney(surfaceForm: String) -> Bool{
        let lowerCase = surfaceForm.lowercased()
        return lowerCase.starts(with: "dolar") || lowerCase.starts(with: "sterlin") || lowerCase.starts(with: "paunt") ||
            lowerCase.starts(with: "ons") || lowerCase.starts(with: "ruble") || lowerCase.starts(with: "mark") ||
            lowerCase.starts(with: "frank") || lowerCase == "yen" || lowerCase.starts(with: "sent") ||
            lowerCase.starts(with: "cent") || lowerCase.starts(with: "yen'") || lowerCase.contains("$")
    }

    /**
    The isPunctuation method without any argument, it checks name variable whether it is a punctuation || not and
    returns true if so.

    - Returns: true if name is a punctuation.
    */
    public func isPunctuation() -> Bool{
        return self.name == "," || self.name == "." || self.name == "!" || self.name == "?" || self.name == ":" ||
               self.name == ";" || self.name == "\"" || self.name == "''" || self.name == "'" || self.name == "`" ||
               self.name == "``" || self.name == "..." || self.name == "-" || self.name == "--"
    }

    /**
    The isTime method takes a String surfaceForm as an input and after converting it to lower case it checks some
    cases.
    If it is in the form of 12:23:34 || 12:23 it returns true.
    If it starts with name of months; ocak, şubat, mart, nisan, mayıs, haziran, temmuz, ağustos, eylül, ekim, kasım,
    aralık it returns true.
    If it equals to the name of days; pazar, pazartesi, salı, çarşamba, perşembe, cuma, cumartesi it returns true.

    PARAMETERS
    ----------
    surfaceForm : String
        String input to check.

    RETURNS
    -------
    Bool
        true if it presents time, and false otherwise.
    */
    public static func isTime(surfaceForm: String) -> Bool{
        var lowerCase = surfaceForm.lowercased()
        if lowerCase.range(of: "(\\d\\d|\\d):(\\d\\d|\\d):(\\d\\d|\\d)", options: .regularExpression) != nil || lowerCase.range(of: "(\\d\\d|\\d):(\\d\\d|\\d)", options: .regularExpression) != nil{
            return true
        }
        if lowerCase.starts(with: "ocak") || lowerCase.starts(with: "şubat") || lowerCase.starts(with: "mart") ||
            lowerCase.starts(with: "nisan") || lowerCase.starts(with: "mayıs") || lowerCase.starts(with: "haziran") ||
            lowerCase.starts(with: "temmuz") || lowerCase.starts(with: "ağustos") || lowerCase.starts(with: "eylül") ||
            lowerCase.starts(with: "ekim") || lowerCase.starts(with: "kasım") || lowerCase == "aralık"{
            return true
        }
        if lowerCase == "pazar" || lowerCase == "salı" || lowerCase.starts(with: "çarşamba") ||
            lowerCase.starts(with: "perşembe") || lowerCase == "cuma" || lowerCase.starts(with: "cumartesi") || lowerCase.starts(with: "pazartesi"){
            return true
        }
        if lowerCase.contains("'"){
            lowerCase = String(lowerCase[..<lowerCase.range(of: "'")!.lowerBound])
        }
        let time: Int? = Int(lowerCase)
        if time != nil{
            if time! > 1900 && time! < 2200{
                return true
            }
        } else {
            return false
        }
        return false
    }

    /**
    The toWordArray method takes a String sourceArray as an input. First it creates a Word type result list and puts
    items of input sourceArray to this result list.

    - Parameter sourceArray : String list.

    - Returns: Word type list.
    */
    public static func toWordArray(sourceArray: [String]) -> [Word]{
        var result : [Word] = []
        for word in sourceArray{
            result.append(Word(name: word))
        }
        return result
    }

    /**
    The toCharacters method creates a Word type characters list and adds characters of name variable
    to newly created list.

    - Returns: Word type list.
    */
    public func toCharacters() -> [Word]{
        var characters : [Word] = []
        for i in 0..<self.name.count{
            let ch = Word.charAt(s: self.name, i: i)
            characters.append(Word(name: String(ch)))
        }
        return characters
    }
}

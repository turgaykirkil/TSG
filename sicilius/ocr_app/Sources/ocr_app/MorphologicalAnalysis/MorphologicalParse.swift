//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 4.03.2021.
//

import Foundation


public class MorphologicalParse{
    
    internal var inflectionalGroups: [InflectionalGroup] = []
    internal var root: Word = Word(name: "")
    
    /**
     * An empty constructor of {@link MorphologicalParse} class.
     */
    public init(){
        
    }
    
    /**
     * Another constructor of {@link MorphologicalParse} class which takes a {@link String} parse as an input. First it creates
     * an {@link ArrayList} as iGs for inflectional groups, and while given String contains derivational boundary (^DB+), it
     * adds the substring to the iGs {@link ArrayList} and continue to use given String from 4th index. If it does not contain ^DB+,
     * it directly adds the given String to the iGs {@link ArrayList}. Then, it creates a new {@link ArrayList} as
     * inflectionalGroups and checks for some cases.
     * <p>
     * If the first item of iGs {@link ArrayList} is ++Punc, it creates a new root as +, and by calling
     * {@link InflectionalGroup} method with Punc it initializes the IG {@link ArrayList} by parsing given input
     * String IG by + and calling the getMorphologicalTag method with these substrings. If getMorphologicalTag method returns
     * a tag, it adds this tag to the IG {@link ArrayList} and also to the inflectionalGroups {@link ArrayList}.
     * <p>
     * If the first item of iGs {@link ArrayList} has +, it creates a new word of first item's substring from index 0 to +,
     * and assigns it to root. Then, by calling {@link InflectionalGroup} method with substring from index 0 to +,
     * it initializes the IG {@link ArrayList} by parsing given input String IG by + and calling the getMorphologicalTag
     * method with these substrings. If getMorphologicalTag method returns a tag, it adds this tag to the IG {@link ArrayList}
     * and also to the inflectionalGroups {@link ArrayList}.
     * <p>
     * If the first item of iGs {@link ArrayList} does not contain +, it creates a new word with first item and assigns it as root.
     * <p>
     * At the end, it loops through the items of iGs and by calling {@link InflectionalGroup} method with these items
     * it initializes the IG {@link ArrayList} by parsing given input String IG by + and calling the getMorphologicalTag
     * method with these substrings. If getMorphologicalTag method returns a tag, it adds this tag to the IG {@link ArrayList}
     * and also to the inflectionalGroups {@link ArrayList}.
     
        - Parameters:
            - parse: String input.
     */
    public init(parse: String){
        var iGs: [String] = []
        var st: String = parse
        while st.contains("^DB+") {
            let index : String.Index = st.firstIndex(of: "^")!
            iGs.append(String(st[..<index]))
            st = String(st[st.index(index, offsetBy: 4)...])
        }
        iGs.append(st)
        if iGs[0] == "++Punc" {
            root = Word(name: "+")
            inflectionalGroups.append(InflectionalGroup(IG: "Punc"))
        } else {
            if iGs[0].contains("+") {
                root =  Word(name: String(iGs[0][..<iGs[0].firstIndex(of: "+")!]))
                let ig = String(iGs[0][iGs[0].index(after: iGs[0].firstIndex(of: "+")!)...])
                let inflectionalGroup = InflectionalGroup(IG: ig)
                inflectionalGroups.append(inflectionalGroup)
            } else {
                root = Word(name: iGs[0])
            }
            for i in 1..<iGs.count {
                inflectionalGroups.append(InflectionalGroup(IG: iGs[i]))
            }
        }
    }
    
    /**
     * Another constructor of {@link MorphologicalParse} class which takes an {@link ArrayList} inflectionalGroups as an input.
     * First, it initializes inflectionalGroups {@link ArrayList} and if the first item of the {@link ArrayList} has +, it gets
     * the substring from index 0 to + and assigns it as root, and by calling {@link InflectionalGroup} method with substring from index 0 to +,
     * it initializes the IG {@link ArrayList} by parsing given input String IG by + and calling the getMorphologicalTag
     * method with these substrings. If getMorphologicalTag method returns a tag, it adds this tag to the IG {@link ArrayList}
     * and also to the inflectionalGroups {@link ArrayList}. However, if the first item does not contain +, it directly prints out
     * indicating that there is no root for that item of this Inflectional Group.
     * <p>
     * At the end, it loops through the items of inflectionalGroups and by calling {@link InflectionalGroup} method with these items
     * it initializes the IG {@link ArrayList} by parsing given input String IG by + and calling the getMorphologicalTag
     * method with these substrings. If getMorphologicalTag method returns a tag, it adds this tag to the IG {@link ArrayList}
     * and also to the inflectionalGroups {@link ArrayList}.
     
        - Parameters:
            - inflectionalGroups: {@link ArrayList} input.
     */
    public init(inflectionalGroups: [String]){
        if inflectionalGroups[0].contains("+") {
            root = Word(name: String(inflectionalGroups[0][..<inflectionalGroups[0].firstIndex(of: "+")!]));
            self.inflectionalGroups.append(InflectionalGroup(IG: String(inflectionalGroups[0][inflectionalGroups[0].index(after: inflectionalGroups[0].firstIndex(of: "+")!)...])))
        }
        for i in 1..<inflectionalGroups.count {
            self.inflectionalGroups.append(InflectionalGroup(IG: inflectionalGroups[i]))
        }
    }
    
    /**
     * The getTransitionList method gets the first item of inflectionalGroups {@link ArrayList} as a {@link String}, then loops
     * through the items of inflectionalGroups and concatenates them by using +.
     
        - Returns: String that contains transition list.
     */
    public func getTransitionList()-> String{
        var result: String = inflectionalGroups[0].description()
        for i in 1..<inflectionalGroups.count {
            result = result + "+" + inflectionalGroups[i].description()
        }
        return result
    }
    
    /**
     * The getInflectionalGroupString method takes an {@link Integer} index as an input and if index is 0, it directly returns the
     * root and the first item of inflectionalGroups {@link ArrayList}. If the index is not 0, it then returns the corresponding
     * item of inflectionalGroups {@link ArrayList} as a {@link String}.
     *
        - Parameters:
            - index Integer input.
        - Returns: Corresponding item of inflectionalGroups at given index as a {@link String}.
     */
    public func getInflectionalGroupString(index: Int) -> String{
        if index == 0 {
            return root.getName() + "+" + inflectionalGroups[0].description()
        } else {
            return inflectionalGroups[index].description()
        }
    }
    
    /**
     * The getInflectionalGroup method takes an {@link Integer} index as an input and it directly returns the {@link InflectionalGroup}
     * at given index.
     *
        - Parameters:
            - index Integer input.
        - Returns: InflectionalGroup at given index.
     */
    public func getInflectionalGroup(index: Int) -> InflectionalGroup{
        return inflectionalGroups[index]
    }
    
    /**
     * The getLastInflectionalGroup method directly returns the last {@link InflectionalGroup} of inflectionalGroups {@link ArrayList}.

        - Returns: The last {@link InflectionalGroup} of inflectionalGroups {@link ArrayList}.
     */
    public func getLastInflectionalGroup() -> InflectionalGroup{
        return inflectionalGroups.last!
    }
    
    /**
     * The getTag method takes an {@link Integer} index as an input and and if the given index is 0, it directly return the root.
     * then, it loops through the inflectionalGroups {@link ArrayList} it returns the MorphologicalTag of the corresponding inflectional group.
        - Parameters:
            - index: Integer input.
     *  - Returns: The MorphologicalTag of the corresponding inflectional group, or null of invalid index inputs.
     */
    public func getTag(index: Int) -> String{
        var size: Int = 1
        if index == 0{
            return root.getName()
        }
        for group in inflectionalGroups {
            if index < size + group.size() {
                return InflectionalGroup.getTag(tag: group.getTag(index: index - size))!
            }
            size += group.size()
        }
        return ""
    }
    
    /**
     * The tagSize method loops through the inflectionalGroups {@link ArrayList} and accumulates the sizes of each inflectional group
     * in the inflectionalGroups.
        - Returns: Ttotal size of the inflectionalGroups {@link ArrayList}.
     */
    public func tagSize() -> Int{
        var size : Int = 1
        for group in inflectionalGroups {
            size += group.size()
        }
        return size
    }
    
    /**
     * The size method returns the size of the inflectionalGroups {@link ArrayList}.
     - Returns: The size of the inflectionalGroups {@link ArrayList}.
     */
    public func size() -> Int{
        return inflectionalGroups.count
    }
    
    /**
     * The firstInflectionalGroup method returns the first inflectional group of inflectionalGroups {@link ArrayList}.
        - Returns: The first inflectional group of inflectionalGroups {@link ArrayList}.
     */
    public func firstInflectionalGroup() -> InflectionalGroup{
        return inflectionalGroups.first!
    }
    
    /**
     * The lastInflectionalGroup method directly returns the last {@link InflectionalGroup} of inflectionalGroups {@link ArrayList}.

        - Returns: The last {@link InflectionalGroup} of inflectionalGroups {@link ArrayList}.
     */
    public func lastInflectionalGroup() -> InflectionalGroup{
        return inflectionalGroups.last!
    }
    
    /**
     * The getWordWithPos method returns root with the MorphologicalTag of the first inflectional as a new word.
        - Returns: Root with the MorphologicalTag of the first inflectional as a new word.
     */
    public func getWordWithPos() -> Word{
        return Word(name: root.getName() + "+" + InflectionalGroup.getTag(tag: firstInflectionalGroup().getTag(index: 0))!)
    }
    
    /**
     * The getPos method returns the MorphologicalTag of the last inflectional group.
        - Returns: The MorphologicalTag of the last inflectional group.
     */
    public func getPos() -> String{
        return InflectionalGroup.getTag(tag: lastInflectionalGroup().getTag(index: 0))!
    }
    
    /**
     * The getRootPos method returns the MorphologicalTag of the first inflectional group.
     - Returns: The MorphologicalTag of the first inflectional group.
     */
    public func getRootPos() -> String{
        return InflectionalGroup.getTag(tag: firstInflectionalGroup().getTag(index: 0))!
    }
    
    /**
     * The lastIGContainsCase method returns the MorphologicalTag of last inflectional group if it is one of the NOMINATIVE,
     * ACCUSATIVE, DATIVE, LOCATIVE or ABLATIVE cases, null otherwise.
        - Returns: Tthe MorphologicalTag of last inflectional group if it is one of the NOMINATIVE,
     * ACCUSATIVE, DATIVE, LOCATIVE or ABLATIVE cases, null otherwise.
     */
    public func lastIGContainsCase() -> String{
        let caseTag = lastInflectionalGroup().containsCase()
        if caseTag != nil{
            return InflectionalGroup.getTag(tag: caseTag!)!
        } else {
            return "NULL"
        }
    }
    
    /**
     * The lastIGContainsTag method takes a MorphologicalTag as an input and returns true if the last inflectional group's
     * MorphologicalTag matches with one of the tags in the IG {@link ArrayList}, falze otherwise.
        - Parameters:
            - tag: {@link MorphologicalTag} type input.
        - Returns: True if the last inflectional group's MorphologicalTag matches with one of the tags in the IG {@link ArrayList}, false otherwise.
     */
    public func lastIGContainsTag(tag: MorphologicalTag) -> Bool{
        return lastInflectionalGroup().containsTag(tag: tag)
    }
    
    /**
     * lastIGContainsPossessive method returns true if the last inflectional group contains one of the
     * possessives: P1PL, P1SG, P2PL, P2SG, P3PL AND P3SG, false otherwise.
        - Returns: True if the last inflectional group contains one of the possessives: P1PL, P1SG, P2PL, P2SG, P3PL AND P3SG, false otherwise.
     */
    public func lastIGContainsPossessive() -> Bool{
        return lastInflectionalGroup().containsPossessive()
    }
    
    /**
     * The isNoun method returns true if the past of speech is NOUN, false otherwise.
        - Returns: True if the part of speech is NOUN, false otherwise.
     */
    public func isNoun() -> Bool{
        return getPos() == "NOUN"
    }
    
    /**
     * The isVerb method returns true if the past of speech is VERB, false otherwise.
        - Returns: True if the part of speech is VERB, false otherwise.
     */
    public func isVerb() -> Bool{
        return getPos() == "VERB"
    }
    
    /**
     * The isRootVerb method returns true if the past of speech of root is BERV, false otherwise.
        - Returns: Ttrue if the part of speech of root is VERB, false otherwise.
     */
    public func isRootVerb() -> Bool{
        return getRootPos() == "VERB"
    }
    
    /**
     * The isAdjective method returns true if the past of speech is ADJ, false otherwise.
        - Returns: True if the part of speech is ADJ, false otherwise.
     */
    public func isAdjective() -> Bool{
        return getPos() == "ADJ"
    }
    
    /**
     * The isProperNoun method returns true if the first inflectional group's MorphologicalTag is a PROPERNOUN, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a PROPERNOUN, false otherwise.
     */
    public func isProperNoun() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.PROPERNOUN)
    }
    
    /**
     * The isPunctuation method returns true if the first inflectional group's MorphologicalTag is a PUNCTUATION, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a PUNCTUATION, false otherwise.
     */
    public func isPunctuation() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.PUNCTUATION)
    }
    
    /**
     * The isCardinal method returns true if the first inflectional group's MorphologicalTag is a CARDINAL, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a CARDINAL, false otherwise.
     */
    public func isCardinal() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.CARDINAL)
    }
    
    /**
     * The isOrdinal method returns true if the first inflectional group's MorphologicalTag is a ORDINAL, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a ORDINAL, false otherwise.
     */
    public func isOrdinal() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.ORDINAL)
    }
    
    /**
     * The isReal method returns true if the first inflectional group's MorphologicalTag is a REAL, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a REAL, false otherwise.
     */
    public func isReal() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.REAL)
    }
    
    /**
     * The isNumber method returns true if the first inflectional group's MorphologicalTag is REAL or CARDINAL, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a REAL or CARDINAL, false otherwise.
     */
    public func isNumber() -> Bool{
        return isReal() || isCardinal()
    }
    
    /**
     * The isTime method returns true if the first inflectional group's MorphologicalTag is a TIME, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a TIME, false otherwise.
     */
    public func isTime() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.TIME)
    }
    
    /**
     * The isDate method returns true if the first inflectional group's MorphologicalTag is a DATE, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a DATE, false otherwise.
     */
    public func isDate() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.DATE)
    }
    
    /**
     * The isHashTag method returns true if the first inflectional group's MorphologicalTag is a HASHTAG, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a HASHTAG, false otherwise.
     */
    public func isHashTag() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.HASHTAG)
    }
    
    /**
     * The isEmail method returns true if the first inflectional group's MorphologicalTag is a EMAIL, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a EMAIL, false otherwise.
     */
    public func isEmail() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.EMAIL)
    }
    
    /**
     * The isPercent method returns true if the first inflectional group's MorphologicalTag is a PERCENT, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a PERCENT, false otherwise.
     */
    public func isPercent() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.PERCENT)
    }
    
    /**
     * The isFraction method returns true if the first inflectional group's MorphologicalTag is a FRACTION, false otherwise.
        - Returns: True if the first inflectional group's MorphologicalTag is a FRACTION, false otherwise.
     */
    public func isFraction() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.FRACTION)
    }
    
    /**
     * The isRange method returns true if the first inflectional group's MorphologicalTag is a RANGE, false otherwise.
        - Returns: Ttrue if the first inflectional group's MorphologicalTag is a RANGE, false otherwise.
     */
    public func isRange() -> Bool{
        return getInflectionalGroup(index: 0).containsTag(tag: MorphologicalTag.RANGE)
    }
    
    /**
     * The isPlural method returns true if {@link InflectionalGroup}'s MorphologicalTags are from the agreement plural
     * or possessive plural, i.e A1PL, A2PL, A3PL, P1PL, P2PL or P3PL, and false otherwise.
        - Returns: True if {@link InflectionalGroup}'s MorphologicalTags are from the agreement plural or possessive plural.
     */
    public func isPlural() -> Bool{
        for inflectionalGroup in inflectionalGroups{
            if inflectionalGroup.containsPlural() {
                return true
            }
        }
        return false
    }
    
    /**
     * The isAuxiliary method returns true if the root equals to the et, ol, or yap, and false otherwise.
        - Returns: True if the root equals to the et, ol, or yap, and false otherwise.
     */
    public func isAuxiliary() -> Bool{
        return root.getName() == "et" || root.getName() == "ol" || root.getName() == "yap"
    }
    
    /**
     * The containsTag method takes a MorphologicalTag as an input and loops through the inflectionalGroups {@link ArrayList},
     * returns true if the input matches with on of the tags in the IG, false otherwise.
        - Parameters:
            - tag: checked tag
     *  - Returns: True if the input matches with on of the tags in the IG, false otherwise.
     */
    public func containsTag(tag: MorphologicalTag) -> Bool{
        for inflectionalGroup in inflectionalGroups {
            if inflectionalGroup.containsTag(tag: tag) {
                return true
            }
        }
        return false
    }
    
    /**
     * The getTreePos method returns the tree pos tag of a morphological analysis.
        - Returns: Tree pos tag of the morphological analysis in string form.
     */
    public func getTreePos() -> String{
        if isProperNoun(){
            return "NP"
        } else {
            if root.getName() == "değil"{
                return "NEG"
            } else {
                if isVerb(){
                    if lastIGContainsTag(tag: MorphologicalTag.ZERO){
                        return "NOMP"
                    } else {
                        return "VP"
                    }
                } else {
                    if isAdjective(){
                        return "ADJP"
                    } else {
                        if isNoun() || isPercent(){
                            return "NP"
                        } else {
                            if containsTag(tag: MorphologicalTag.ADVERB){
                                return "ADVP"
                            } else {
                                if isNumber() || isFraction(){
                                    return "NUM"
                                } else {
                                    if containsTag(tag: MorphologicalTag.POSTPOSITION){
                                        return "PP"
                                    } else {
                                        if containsTag(tag: MorphologicalTag.CONJUNCTION){
                                            return "CONJP"
                                        } else {
                                            if containsTag(tag: MorphologicalTag.DETERMINER){
                                                return "DP"
                                            } else {
                                                if containsTag(tag: MorphologicalTag.INTERJECTION){
                                                    return "INTJP"
                                                } else {
                                                    if containsTag(tag: MorphologicalTag.QUESTIONPRONOUN){
                                                        return "WP"
                                                    } else {
                                                        if containsTag(tag: MorphologicalTag.PRONOUN){
                                                            return "NP"
                                                        } else {
                                                            if isPunctuation(){
                                                                switch (root.getName()){
                                                                    case "!", "?":
                                                                        return "."
                                                                    case ";", "-", "--":
                                                                        return ":"
                                                                    case "(", "-LRB-", "-lrb-":
                                                                        return "-LRB-"
                                                                    case ")", "-RRB-", "-rrb-":
                                                                        return "-RRB-"
                                                                    default:
                                                                        return root.getName()
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        return "-XXX-"
    }
    
    /**
     * The no-arg getWord method returns root {@link Word}.

        - Returns: Root {@link Word}.
     */
    public func getWord() -> Word{
        return root;
    }
    
    public func description() -> String{
        var result: String = root.getName() + "+" + inflectionalGroups[0].description()
        for i in 1..<inflectionalGroups.count{
            result = result + "^DB+" + inflectionalGroups[i].description()
        }
        return result;
    }
    
}

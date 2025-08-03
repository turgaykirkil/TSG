//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 4.03.2021.
//

import Foundation

public class InflectionalGroup{
    
    private var IG : [MorphologicalTag] = []
    
    static var tags : [String] = ["NOUN", "ADV", "ADJ", "VERB", "A1SG",
    "A2SG", "A3SG", "A1PL", "A2PL", "A3PL",
    "P1SG", "P2SG", "P3SG", "P1PL", "P2PL",
    "P3PL", "PROP", "PNON", "NOM", "WITH",
    "WITHOUT", "ACC", "DAT", "GEN", "ABL",
    "ZERO", "ABLE", "NEG", "PAST",
    "CONJ", "DET", "DUP", "INTERJ", "NUM",
    "POSTP", "PUNC", "QUES", "AGT", "BYDOINGSO",
    "CARD", "CAUS", "DEMONSP", "DISTRIB", "FITFOR",
    "FUTPART", "INF", "NESS", "ORD", "PASS",
    "PASTPART", "PRESPART", "QUESP", "QUANTP", "RANGE",
    "RATIO", "REAL", "RECIP", "REFLEX", "REFLEXP",
    "TIME", "WHEN", "WHILE", "WITHOUTHAVINGDONESO", "PCABL",
    "PCACC", "PCDAT", "PCGEN", "PCINS", "PCNOM",
    "ACQUIRE", "ACTOF", "AFTERDOINGSO", "ALMOST", "AS",
    "ASIF", "BECOME", "EVERSINCE", "FEELLIKE", "HASTILY",
    "INBETWEEN", "JUSTLIKE", "LY", "NOTABLESTATE", "RELATED",
    "REPEAT", "SINCE", "SINCEDOINGSO", "START", "STAY",
    "EQU", "INS", "AOR", "DESR", "FUT",
    "IMP", "NARR", "NECES", "OPT", "PAST",
    "PRES", "PROG1", "PROG2", "COND", "COP",
    "POS", "PRON", "LOC", "REL", "DEMONS",
    "INF2", "INF3", "BSTAG", "ESTAG", "BTTAG",
    "ETTAG", "BDTAG", "EDTAG", "INF1", "ASLONGAS",
    "DIST", "ADAMANTLY", "PERCENT", "WITHOUTBEINGABLETOHAVEDONESO", "DIM",
    "PERS", "FRACTION", "HASHTAG", "EMAIL", "DATE", "CODE", "METRIC"]
    
    static var morphoTags : [MorphologicalTag] = [MorphologicalTag.NOUN, MorphologicalTag.ADVERB, MorphologicalTag.ADJECTIVE,
    MorphologicalTag.VERB, MorphologicalTag.A1SG, MorphologicalTag.A2SG, MorphologicalTag.A3SG, MorphologicalTag.A1PL,
    MorphologicalTag.A2PL, MorphologicalTag.A3PL, MorphologicalTag.P1SG, MorphologicalTag.P2SG, MorphologicalTag.P3SG, MorphologicalTag.P1PL,
    MorphologicalTag.P2PL, MorphologicalTag.P3PL, MorphologicalTag.PROPERNOUN, MorphologicalTag.PNON, MorphologicalTag.NOMINATIVE,
    MorphologicalTag.WITH, MorphologicalTag.WITHOUT, MorphologicalTag.ACCUSATIVE, MorphologicalTag.DATIVE, MorphologicalTag.GENITIVE,
    MorphologicalTag.ABLATIVE, MorphologicalTag.ZERO, MorphologicalTag.ABLE, MorphologicalTag.NEGATIVE, MorphologicalTag.PASTTENSE,
    MorphologicalTag.CONJUNCTION, MorphologicalTag.DETERMINER, MorphologicalTag.DUPLICATION, MorphologicalTag.INTERJECTION, MorphologicalTag.NUMBER,
    MorphologicalTag.POSTPOSITION, MorphologicalTag.PUNCTUATION, MorphologicalTag.QUESTION, MorphologicalTag.AGENT, MorphologicalTag.BYDOINGSO,
    MorphologicalTag.CARDINAL, MorphologicalTag.CAUSATIVE, MorphologicalTag.DEMONSTRATIVEPRONOUN, MorphologicalTag.DISTRIBUTIVE, MorphologicalTag.FITFOR,
    MorphologicalTag.FUTUREPARTICIPLE, MorphologicalTag.INFINITIVE, MorphologicalTag.NESS, MorphologicalTag.ORDINAL, MorphologicalTag.PASSIVE,
    MorphologicalTag.PASTPARTICIPLE, MorphologicalTag.PRESENTPARTICIPLE, MorphologicalTag.QUESTIONPRONOUN, MorphologicalTag.QUANTITATIVEPRONOUN, MorphologicalTag.RANGE,
    MorphologicalTag.RATIO, MorphologicalTag.REAL, MorphologicalTag.RECIPROCAL, MorphologicalTag.REFLEXIVE, MorphologicalTag.REFLEXIVEPRONOUN,
    MorphologicalTag.TIME, MorphologicalTag.WHEN, MorphologicalTag.WHILE, MorphologicalTag.WITHOUTHAVINGDONESO, MorphologicalTag.PCABLATIVE,
    MorphologicalTag.PCACCUSATIVE, MorphologicalTag.PCDATIVE, MorphologicalTag.PCGENITIVE, MorphologicalTag.PCINSTRUMENTAL, MorphologicalTag.PCNOMINATIVE,
    MorphologicalTag.ACQUIRE, MorphologicalTag.ACTOF, MorphologicalTag.AFTERDOINGSO, MorphologicalTag.ALMOST, MorphologicalTag.AS,
    MorphologicalTag.ASIF, MorphologicalTag.BECOME, MorphologicalTag.EVERSINCE, MorphologicalTag.FEELLIKE, MorphologicalTag.HASTILY,
    MorphologicalTag.INBETWEEN, MorphologicalTag.JUSTLIKE, MorphologicalTag.LY, MorphologicalTag.NOTABLESTATE, MorphologicalTag.RELATED,
    MorphologicalTag.REPEAT, MorphologicalTag.SINCE, MorphologicalTag.SINCEDOINGSO, MorphologicalTag.START, MorphologicalTag.STAY,
    MorphologicalTag.EQUATIVE, MorphologicalTag.INSTRUMENTAL, MorphologicalTag.AORIST, MorphologicalTag.DESIRE, MorphologicalTag.FUTURE,
    MorphologicalTag.IMPERATIVE, MorphologicalTag.NARRATIVE, MorphologicalTag.NECESSITY, MorphologicalTag.OPTATIVE, MorphologicalTag.PAST,
    MorphologicalTag.PRESENT, MorphologicalTag.PROGRESSIVE1, MorphologicalTag.PROGRESSIVE2, MorphologicalTag.CONDITIONAL, MorphologicalTag.COPULA,
    MorphologicalTag.POSITIVE, MorphologicalTag.PRONOUN, MorphologicalTag.LOCATIVE, MorphologicalTag.RELATIVE, MorphologicalTag.DEMONSTRATIVE,
    MorphologicalTag.INFINITIVE2, MorphologicalTag.INFINITIVE3, MorphologicalTag.BEGINNINGOFSENTENCE, MorphologicalTag.ENDOFSENTENCE, MorphologicalTag.BEGINNINGOFTITLE,
    MorphologicalTag.ENDOFTITLE, MorphologicalTag.BEGINNINGOFDOCUMENT, MorphologicalTag.ENDOFDOCUMENT, MorphologicalTag.INFINITIVE, MorphologicalTag.ASLONGAS,
    MorphologicalTag.DISTRIBUTIVE, MorphologicalTag.ADAMANTLY, MorphologicalTag.PERCENT, MorphologicalTag.WITHOUTBEINGABLETOHAVEDONESO, MorphologicalTag.DIMENSION,
    MorphologicalTag.PERSONALPRONOUN, MorphologicalTag.FRACTION, MorphologicalTag.HASHTAG, MorphologicalTag.EMAIL, MorphologicalTag.DATE,
                                                  MorphologicalTag.CODE, MorphologicalTag.METRIC]
    
    /**
     * The getMorphologicalTag method takes a String tag as an input and if the input matches with one of the elements of
     * tags array, it then gets the morphoTags of this tag and returns it.

        - Parameters:
            - tag: String to get morphoTags from.
        - Returns: MorphoTags if found, nil otherwise.
     */
    public static func getMorphologicalTag(tag: String) -> MorphologicalTag?{
        for j in 0..<tags.count {
            if tag.lowercased() == tags[j].lowercased() {
                return morphoTags[j]
            }
        }
        return nil
    }
    
    /**
     * The getTag method takes a MorphologicalTag type tag as an input and returns its corresponding tag from tags array.

        - Parameters:
            - tag: MorphologicalTag type input to find tag from.
        - Returns: Tag if found, nil otherwise.
     */
    public static func getTag(tag: MorphologicalTag) -> String?{
        for j in 0..<morphoTags.count {
            if tag == morphoTags[j] {
                return tags[j]
            }
        }
        return nil
    }
    
    /**
     * A constructor of {@link InflectionalGroup} class which initializes the IG {@link ArrayList} by parsing given input
     * String IG by + and calling the getMorphologicalTag method with these substrings. If getMorphologicalTag method returns
     * a tag, it adds this tag to the IG {@link ArrayList}.

        - Parameters:
            - IG: String input.
     */
    public init(IG: String){
        var st: String = IG
        while st.contains("+") {
            let morphologicalTag = String(st[..<st.firstIndex(of: "+")!])
            let tag = InflectionalGroup.getMorphologicalTag(tag: morphologicalTag)
            if tag != nil {
                self.IG.append(tag!)
            }
            st = String(st[st.index(after: st.firstIndex(of: "+")!)...])
        }
        let morphologicalTag = st
        let tag = InflectionalGroup.getMorphologicalTag(tag: morphologicalTag)
        if tag != nil {
            self.IG.append(tag!)
        }
    }
    
    /**
     * Another getTag method which takes index as an input and returns the corresponding tag from IG {@link Array}.

        - Parameters:
            - index: to get tag.
        - Returns: Tag at input index.
     */
    public func getTag(index: Int) -> MorphologicalTag{
        return IG[index]
    }
    
    /**
     * The size method returns the size of the IG {@link ArrayList}.

        - Returns: the size of the IG {@link ArrayList}.
     */
    public func size() -> Int{
        return IG.count
    }
    
    public func description() -> String{
        var result: String = InflectionalGroup.getTag(tag: self.IG[0])!
        for i in 1..<IG.count {
            result = result + "+" + InflectionalGroup.getTag(tag: self.IG[i])!
        }
        return result
    }
    
    /**
     * The containsCase method loops through the tags in IG {@link ArrayList} and finds out the tags of the NOMINATIVE,
     * ACCUSATIVE, DATIVE, LOCATIVE or ABLATIVE cases.

        - Returns: Tag which holds the condition.
     */
    public func containsCase() -> MorphologicalTag?{
        for tag in self.IG{
            if tag == MorphologicalTag.NOMINATIVE || tag == MorphologicalTag.ACCUSATIVE
                || tag == MorphologicalTag.DATIVE || tag == MorphologicalTag.LOCATIVE
                || tag == MorphologicalTag.ABLATIVE{
                return tag
            }
        }
        return nil
    }
    
    /**
     * The containsPlural method loops through the tags in IG {@link ArrayList} and checks whether the tags are from
     * the agreement plural or possessive plural, i.e A1PL, A2PL, A3PL, P1PL, P2PL and P3PL.

        - Returns: True if the tag is plural, false otherwise.
     */
    public func containsPlural() -> Bool{
        for tag in self.IG{
            if tag == MorphologicalTag.A1PL || tag == MorphologicalTag.A2PL
                || tag == MorphologicalTag.A3PL || tag == MorphologicalTag.P1PL
                || tag == MorphologicalTag.P2PL || tag == MorphologicalTag.P3PL{
                return true
            }
        }
        return false
    }
    
    /**
     * The containsTag method takes a MorphologicalTag type tag as an input and loops through the tags in
     * IG {@link ArrayList} and returns true if the input matches with on of the tags in the IG.

        - Parameters:
            - tag: MorphologicalTag type input to search for.
        - Returns: True if tag matches with the tag in IG, false otherwise.
     */
    public func containsTag(tag: MorphologicalTag) -> Bool{
        for currentTag in self.IG{
            if tag == currentTag{
                return true
            }
        }
        return false
    }
    
    /**
     * The containsPossessive method loops through the tags in IG {@link ArrayList} and returns true if the tag in IG is
     * one of the possessives: P1PL, P1SG, P2PL, P2SG, P3PL AND P3SG.

        - Returns: True if it contains possessive tag, false otherwise.
     */
    public func containsPossessive() -> Bool{
        for tag in self.IG{
            if tag == MorphologicalTag.P1PL || tag == MorphologicalTag.P1SG
                || tag == MorphologicalTag.P2PL || tag == MorphologicalTag.P2SG
                || tag == MorphologicalTag.P3PL || tag == MorphologicalTag.P3SG{
                return true
            }
        }
        return false
    }

}

//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 9.03.2021.
//

import Foundation


public class FsmParseList{
    
    private var fsmParses: [FsmParse] = []
    static var longestRootExceptions: [String] = ["acağı acak NOUN VERB", "acağım acak NOUN VERB", "acağımı acak NOUN VERB", "acağımız acak NOUN VERB",
                                                  "acağın acak NOUN VERB",
                                                  "acağına acak NOUN VERB", "acağını acak NOUN VERB", "acağının acak NOUN VERB", "acağınız acak NOUN VERB",
                                                  "acağınıza acak NOUN VERB",
                                                  "acağınızdır acak NOUN VERB", "acağınızı acak NOUN VERB", "acağınızın acak NOUN VERB", "acağız acak NOUN VERB",
                                                  "acakları acak NOUN VERB",
                                                  "acaklarını acak NOUN VERB", "acaksa acak NOUN VERB", "acaktır acak NOUN VERB", "ardım ar NOUN VERB",
                                                  "arız ar NOUN VERB",
                                                  "arken ar NOUN VERB", "arsa ar NOUN VERB", "arsak ar NOUN VERB", "arsanız ar NOUN VERB", "arsınız ar NOUN VERB",
                                                  "eceği ecek NOUN VERB", "eceğim ecek NOUN VERB", "eceğimi ecek NOUN VERB", "eceğimiz ecek NOUN VERB",
                                                  "eceğin ecek NOUN VERB",
                                                  "eceğine ecek NOUN VERB", "eceğini ecek NOUN VERB", "eceğinin ecek NOUN VERB", "eceğiniz ecek NOUN VERB",
                                                  "eceğinizdir ecek NOUN VERB",
                                                  "eceğinize ecek NOUN VERB", "eceğinizi ecek NOUN VERB", "eceğinizin ecek NOUN VERB", "eceğiz ecek NOUN VERB",
                                                  "ecekleri ecek NOUN VERB",
                                                  "eceklerini ecek NOUN VERB", "ecekse ecek NOUN VERB", "ecektir ecek NOUN VERB", "erdim er NOUN VERB",
                                                  "eriz er NOUN VERB",
                                                  "erken er NOUN VERB", "erse er NOUN VERB", "ersek er NOUN VERB", "erseniz er NOUN VERB", "ersiniz er NOUN VERB",
                                                  "ilen i VERB VERB", "ilene i VERB VERB", "ilin i VERB VERB", "ilince i VERB VERB", "imiz i ADJ NOUN",
                                                  "in i ADJ NOUN", "inde i ADJ NOUN", "ine i ADJ NOUN", "ini i ADJ NOUN", "inin i ADJ NOUN",
                                                  "ılan ı NOUN VERB", "ılana ı NOUN VERB", "ılın ı NOUN VERB", "ılınca ı NOUN VERB", "la la VERB NOUN",
                                                  "lar la VERB NOUN", "lardan la VERB NOUN", "lardandır la VERB NOUN", "lardır la VERB NOUN", "ları la VERB NOUN",
                                                  "larıdır la VERB NOUN", "larım la VERB NOUN", "larımda la VERB NOUN", "larımdan la VERB NOUN", "larımız la VERB NOUN",
                                                  "larımıza la VERB NOUN",
                                                  "larımızda la VERB NOUN", "larımızdan la VERB NOUN", "larımızdaydı la VERB NOUN", "larımızı la VERB NOUN",
                                                  "larımızın la VERB NOUN",
                                                  "larımızla la VERB NOUN", "ların la VERB NOUN", "larına la VERB NOUN", "larında la VERB NOUN",
                                                  "larındaki la VERB NOUN",
                                                  "larındakiler la VERB NOUN", "larındakilere la VERB NOUN", "larındakileri la VERB NOUN",
                                                  "larındakilerin la VERB NOUN", "larından la VERB NOUN",
                                                  "larındandır la VERB NOUN", "larındaysa la VERB NOUN", "larını la VERB NOUN", "larının la VERB NOUN",
                                                  "larınız la VERB NOUN",
                                                  "larınıza la VERB NOUN", "larınızda la VERB NOUN", "larınızdaki la VERB NOUN", "larınızdan la VERB NOUN",
                                                  "larınızı la VERB NOUN",
                                                  "larınızın la VERB NOUN", "larınızla la VERB NOUN", "larıyla la VERB NOUN", "le le VERB NOUN",
                                                  "ler le VERB NOUN",
                                                  "lerden le VERB NOUN", "lerdendir le VERB NOUN", "lerdir le VERB NOUN", "leri le VERB NOUN",
                                                  "leridir le VERB NOUN",
                                                  "lerim le VERB NOUN", "lerimden le VERB NOUN", "lerimiz le VERB NOUN", "lerimizde le VERB NOUN",
                                                  "lerimizden le VERB NOUN",
                                                  "lerimizdeydi le VERB NOUN", "lerimize le VERB NOUN", "lerimizi le VERB NOUN", "lerimizin le VERB NOUN",
                                                  "lerimizle le VERB NOUN",
                                                  "lerin le VERB NOUN", "lerinde le VERB NOUN", "lerindeki le VERB NOUN", "lerindekiler le VERB NOUN",
                                                  "lerindekilere le VERB NOUN",
                                                  "lerindekileri le VERB NOUN", "lerindekilerin le VERB NOUN", "lerinden le VERB NOUN",
                                                  "lerindendir le VERB NOUN", "lerindeyse le VERB NOUN",
                                                  "lerine le VERB NOUN", "lerini le VERB NOUN", "lerinin le VERB NOUN", "leriniz le VERB NOUN",
                                                  "lerinizde le VERB NOUN",
                                                  "lerinizdeki le VERB NOUN", "lerinizden le VERB NOUN", "lerinize le VERB NOUN", "lerinizi le VERB NOUN",
                                                  "lerinizin le VERB NOUN",
                                                  "lerinizle le VERB NOUN", "leriyle le VERB NOUN", "madan ma NOUN VERB", "malı ma NOUN VERB",
                                                  "malıdır ma NOUN VERB", "malıdırlar ma NOUN VERB", "malılar ma NOUN VERB", "malısınız ma NOUN VERB",
                                                  "malıyım ma NOUN VERB",
                                                  "malıyız ma NOUN VERB", "mam ma NOUN VERB", "mama ma NOUN VERB", "mamız ma NOUN VERB", "mamıza ma NOUN VERB",
                                                  "mamızı ma NOUN VERB", "manız ma NOUN VERB", "manızda ma NOUN VERB", "manızdır ma NOUN VERB",
                                                  "manızı ma NOUN VERB",
                                                  "manızla ma NOUN VERB", "ması ma NOUN VERB", "masıdır ma NOUN VERB", "masın ma NOUN VERB",
                                                  "masına ma NOUN VERB",
                                                  "masında ma NOUN VERB", "masındaki ma NOUN VERB", "masını ma NOUN VERB", "masıyla ma NOUN VERB",
                                                  "mdan m NOUN NOUN",
                                                  "meden me NOUN VERB", "meli me NOUN VERB", "melidir me NOUN VERB", "melidirler me NOUN VERB",
                                                  "meliler me NOUN VERB",
                                                  "melisiniz me NOUN VERB", "meliyim me NOUN VERB", "meliyiz me NOUN VERB", "mem me NOUN VERB",
                                                  "meme me NOUN VERB",
                                                  "memiz me NOUN VERB", "memize me NOUN VERB", "memizi me NOUN VERB", "meniz me NOUN VERB",
                                                  "menizde me NOUN VERB",
                                                  "menizdir me NOUN VERB", "menizi me NOUN VERB", "menizle me NOUN VERB", "mesi me NOUN VERB",
                                                  "mesidir me NOUN VERB",
                                                  "mesin me NOUN VERB", "mesinde me NOUN VERB", "mesindeki me NOUN VERB", "mesine me NOUN VERB",
                                                  "mesini me NOUN VERB",
                                                  "mesiyle me NOUN VERB", "mişse miş NOUN VERB", "mını m NOUN NOUN", "mışsa mış NOUN VERB", "mız m NOUN NOUN",
                                                  "na n NOUN NOUN", "ne n NOUN NOUN", "nin n NOUN NOUN", "niz n NOUN NOUN",
                                                  "nın n NOUN NOUN", "nız n NOUN NOUN", "rdim r NOUN VERB", "rdım r NOUN VERB", "riz r NOUN VERB",
                                                  "rız r NOUN VERB", "rken r NOUN VERB", "rken r NOUN VERB", "rsa r NOUN VERB", "rsak r NOUN VERB",
                                                  "rsanız r NOUN VERB", "rse r NOUN VERB", "rsek r NOUN VERB", "rseniz r NOUN VERB", "rsiniz r NOUN VERB",
                                                  "rsınız r NOUN VERB", "sa sa VERB ADJ", "se se VERB ADJ", "ulan u NOUN VERB", "un un VERB NOUN",
                                                  "üne ün VERB NOUN", "unun un VERB NOUN", "ince i NOUN VERB", "unca u NOUN VERB", "ınca ı NOUN VERB",
                                                  "unca un NOUN VERB", "ilen ile VERB VERB"]
    
    /**
     * A constructor of {@link FsmParseList} class which takes an {@link ArrayList} fsmParses as an input. First it sorts
     * the items of the {@link ArrayList} then loops through it, if the current item's transitions equal to the next item's
     * transitions, it removes the latter item. At the end, it assigns this {@link ArrayList} to the fsmParses variable.
        - Parameters:
            - fsmParses: {@link FsmParse} type{@link ArrayList} input.
     */
    public init(fsmParses: [FsmParse]){
        self.fsmParses = fsmParses
        self.fsmParses.sort{$0.transitionList() < $1.transitionList()}
        var i : Int = 0
        while i < self.fsmParses.count - 1 {
            let parse1 = self.fsmParses[i].transitionList()
            let parse2 = self.fsmParses[i + 1].transitionList()
            if parse1 == parse2 {
                self.fsmParses.remove(at: i + 1)
                i -= 1
            }
            i += 1
        }
    }
    
    /**
     * The size method returns the size of fsmParses {@link ArrayList}.
        - Returns: The size of fsmParses {@link ArrayList}.
     */
    public func size() -> Int{
        return fsmParses.count
    }
    
    /**
     * The getFsmParse method takes an integer index as an input and returns the item of fsmParses {@link ArrayList} at given index.
        - Parameters:
            - index: Integer input.
        - Returns: Tthe item of fsmParses {@link ArrayList} at given index.
     */
    public func getFsmParse(index: Int) -> FsmParse{
        return fsmParses[index]
    }
    
    /**
     * The rootWords method gets the first item's root of fsmParses {@link ArrayList} and uses it as currentRoot. Then loops through
     * the fsmParses, if the current item's root does not equal to the currentRoot, it then assigns it as the currentRoot and
     * accumulates root words in a {@link String} result.
     - Returns: String result that has root words.
     */
    public func rootWords() -> String{
        var result: String = fsmParses[0].getWord().getName()
        var currentRoot: String = result
        for i in 1..<fsmParses.count {
            if fsmParses[i].getWord().getName() != currentRoot {
                currentRoot = fsmParses[i].getWord().getName()
                result = result + "$" + currentRoot
            }
        }
        return result
    }
    
    /**
     * The reduceToParsesWithSameRootAndPos method takes a {@link Word} currentWithPos as an input and loops i times till
     * i equals to the size of the fsmParses {@link ArrayList}. If the given currentWithPos does not equal to the ith item's
     * root and the MorphologicalTag of the first inflectional of fsmParses, it removes the ith item from the {@link ArrayList}.
        - Parameters:
            - currentWithPos {@link Word} input.
     */
    public func reduceToParsesWithSameRootAndPos(currentWithPos: Word){
        var i : Int = 0
        while i < fsmParses.count {
            if fsmParses[i].getWordWithPos() != currentWithPos {
                fsmParses.remove(at: i)
            } else {
                i += 1
            }
        }
    }
    
    /**
     * The getParseWithLongestRootWord method returns the parse with the longest root word. If more than one parse has the
     * longest root word, the first parse with that root is returned.
        - Returns: FsmParse Parse with the longest root word.
     */
    public func getParseWithLongestRootWord() -> FsmParse{
        var maxLength: Int = -1
        var bestParse : FsmParse? = nil
        if !fsmParses.isEmpty{
            bestParse = fsmParses[0]
        }
        for currentParse in fsmParses {
            if currentParse.getWord().getName().count > maxLength && !self.isLongestRootException(fsmParse: currentParse){
                maxLength = currentParse.getWord().getName().count
                bestParse = currentParse
            }
        }
        return bestParse!
    }
    
    /**
     * The isLongestRootException method returns true if the longest root word belongs to an exceptional case, false
     * otherwise.
     *   - Parameters:
     *      - fsmParse: FsmParse input
     *   - Returns: true if the longest root belongs to an exceptional case, false otherwise.
     */
    public func isLongestRootException(fsmParse: FsmParse) -> Bool{
        let surfaceForm = fsmParse.getSurfaceForm()
        let root = fsmParse.getWord().getName()
        for longestRootException in FsmParseList.longestRootExceptions{
            let exceptionItems : [String] = longestRootException.split(separator: " ").map(String.init)
            let surfaceFormEnding = exceptionItems[0]
            let longestRootEnding = exceptionItems[1]
            let longestRootPos = exceptionItems[2]
            let possibleRootPos = exceptionItems[3]
            let possibleRoot = surfaceForm.replacingOccurrences(of: surfaceFormEnding, with: "")
            if surfaceForm.hasSuffix(surfaceFormEnding) && root.hasSuffix(longestRootEnding)
                && fsmParse.getRootPos() == longestRootPos{
                for currentParse in fsmParses{
                    if currentParse.getWord().getName() == possibleRoot && currentParse.getRootPos() == possibleRootPos{
                        return true
                    }
                }
            }
        }
        return false
    }
    
    /**
     * The reduceToParsesWithSameRoot method takes a {@link String} currentWithPos as an input and loops i times till
     * i equals to the size of the fsmParses {@link ArrayList}. If the given currentRoot does not equal to the root of ith item of
     * fsmParses, it removes the ith item from the {@link ArrayList}.
        - Parameters:
            - currentRoot: {@link String} input.
     */
    public func reduceToParsesWithSameRoot(currentRoot: String){
        var i : Int = 0
        while i < fsmParses.count {
            if fsmParses[i].getWord().getName() != currentRoot {
                fsmParses.remove(at: i)
            } else {
                i += 1
            }
        }
    }
    
    /**
     * The constructParseListForDifferentRootWithPos method initially creates a result {@link ArrayList} then loops through the
     * fsmParses {@link ArrayList}. For the first iteration, it creates new {@link ArrayList} as initial, then adds the
     * first item od fsmParses to initial and also add this initial {@link ArrayList} to the result {@link ArrayList}.
     * For the following iterations, it checks whether the current item's root with the MorphologicalTag of the first inflectional
     * equal to the previous item's  root with the MorphologicalTag of the first inflectional. If so, it adds that item
     * to the result {@link ArrayList}, if not it creates new {@link ArrayList} as initial and adds the first item od fsmParses
     * to initial and also add this initial {@link ArrayList} to the result {@link ArrayList}.
     - Returns: result {@link ArrayList} type of {@link FsmParseList}.
     */
    public func constructParseListForDifferentRootWithPos() -> [FsmParseList]{
        var result : [FsmParseList] = []
        var i : Int = 0
        while i < fsmParses.count {
            if i == 0 {
                var initial : [FsmParse] = []
                initial.append(fsmParses[i])
                result.append(FsmParseList(fsmParses: initial))
            } else {
                if fsmParses[i].getWordWithPos() == fsmParses[i - 1].getWordWithPos() {
                    result.last!.fsmParses.append(fsmParses[i])
                } else {
                    var initial : [FsmParse] = []
                    initial.append(fsmParses[i])
                    result.append(FsmParseList(fsmParses: initial))
                }
            }
            i += 1
        }
        return result
    }
    
    /**
     * The parsesWithoutPrefixAndSuffix method first creates a {@link String} array named analyses with the size of fsmParses {@link ArrayList}'s size.
     * <p>
     * If the size is just 1, it then returns the first item's transitionList, if it is greater than 1, loops through the fsmParses and
     * puts the transitionList of each item to the analyses array.
     * <p>
     * If the removePrefix condition holds, it loops through the analyses array and takes each item's substring after the first + sign and updates that
     * item of analyses array with that substring.
     * <p>
     * If the removeSuffix condition holds, it loops through the analyses array and takes each item's substring till the last + sign and updates that
     * item of analyses array with that substring.
     * <p>
     * It then removes the duplicate items of analyses array and returns a result {@link String} that has the accumulated items of analyses array.
        - Returns: Result {@link String} that has the accumulated items of analyses array.
     */
    public func parsesWithoutPrefixAndSuffix() -> String{
        var analyses : [String] = []
        var removePrefix : Bool = true
        var removeSuffix :Bool = true
        if fsmParses.count == 1 {
            let st = fsmParses[0].transitionList()
            return String(st[st.index(after: st.firstIndex(of: "+")!)...])
        }
        for i in 0..<fsmParses.count {
            analyses.append(fsmParses[i].transitionList())
        }
        while removePrefix {
            removePrefix = true
            for i in 0..<fsmParses.count - 1 {
                if !analyses[i].contains("+") || !analyses[i + 1].contains("+") || String(analyses[i][...analyses[i].firstIndex(of: "+")!]) != String(analyses[i + 1][...analyses[i + 1].firstIndex(of: "+")!]) {
                    removePrefix = false
                    break
                }
            }
            if removePrefix {
                for i in 0..<fsmParses.count {
                    analyses[i] = String(analyses[i][analyses[i].index(after: analyses[i].firstIndex(of: "+")!)...])
                }
            }
        }
        while removeSuffix {
            removeSuffix = true
            for i in 0..<fsmParses.count - 1 {
                if !analyses[i].contains("+") || !analyses[i + 1].contains("+") || String(analyses[i][analyses[i].index(after: analyses[i].lastIndex(of: "+")!)...]) != String(analyses[i + 1][analyses[i + 1].index(after: analyses[i + 1].lastIndex(of: "+")!)...]) {
                    removeSuffix = false
                    break
                }
            }
            if removeSuffix {
                for i in 0..<fsmParses.count {
                    analyses[i] = String(analyses[i][..<analyses[i].lastIndex(of: "+")!])
                }
            }
        }
        for i in 0..<analyses.count {
            for j in i + 1..<analyses.count {
                if analyses[i] > analyses[j] {
                    let tmp : String = analyses[i]
                    analyses[i] = analyses[j]
                    analyses[j] = tmp
                }
            }
        }
        var result : String = analyses[0]
        for i in 1..<analyses.count {
            result = result + "$" + analyses[i]
        }
        return result
    }
    
    /**
     * The overridden description method loops through the fsmParses {@link ArrayList} and accumulates the items to a result {@link String}.
        - Returns: Result {@link String} that has the items of fsmParses {@link ArrayList}.
     */
    public func description() -> String{
        var result : String = ""
        for i in 0..<fsmParses.count {
            result = result + fsmParses[i].description() + "\n"
        }
        return result
    }
}

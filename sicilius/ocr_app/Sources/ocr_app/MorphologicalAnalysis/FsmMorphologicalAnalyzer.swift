//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 16.03.2021.
//

import Foundation


public class FsmMorphologicalAnalyzer{
    
    private var dictionaryTrie: Trie
    private var parsedSurfaceForms: Set<String>? = nil
    private var finiteStateMachine: FiniteStateMachine
    private static let MAX_DISTANCE: Int = 2
    private var dictionary: TxtDictionary
    private var cache: LRUCache<String, FsmParseList>? = nil
    private var mostUsedPatterns: NSMutableDictionary = [:]

    /**
     * First no-arg constructor of FsmMorphologicalAnalyzer class. It generates a new TxtDictionary type dictionary from
     * turkish_dictionary.txt with fixed cache size 10000000 and by using turkish_finite_state_machine.xml file.
     */
    public convenience init(){
        self.init(fileName: "turkish_finite_state_machine", dictionary: TxtDictionary(), cacheSize: 10000000)
    }
    
    /**
     Another constructor of FsmMorphologicalAnalyzer class. It generates a new TxtDictionary type dictionary from
     turkish_dictionary.txt with given input cacheSize and by using turkish_finite_state_machine.xml file.
     - Parameters:
        - cacheSize: the size of the LRUCache.
     */
    public convenience init(cacheSize: Int){
        self.init(fileName: "turkish_finite_state_machine", dictionary: TxtDictionary(), cacheSize: cacheSize)
    }
    
    /**
     * Another constructor of FsmMorphologicalAnalyzer class. It generates a new TxtDictionary type dictionary from
     * given input dictionary file name and by using turkish_finite_state_machine.xml file.
        - Parameters:
            - dictionaryFileName: the size of the LRUCache.
     */
    public convenience init(dictionaryFileName: String){
        self.init(fileName: "turkish_finite_state_machine", dictionary: TxtDictionary(fileName: dictionaryFileName), cacheSize: 10000000)
    }
    
    /**
     * Another constructor of FsmMorphologicalAnalyzer class. It generates a new TxtDictionary type dictionary from
     * given input dictionary file name and by using turkish_finite_state_machine.xml file.
        - Parameters:
            - fileName:           the file to read the finite state machine.
            - dictionaryFileName: the file to read the dictionary.
     */
    public convenience init(fileName: String, dictionaryFileName: String){
        self.init(fileName: fileName, dictionary: TxtDictionary(fileName: dictionaryFileName), cacheSize: 10000000)
    }
    
    /**
     * Another constructor of FsmMorphologicalAnalyzer class. It generates a new TxtDictionary type dictionary from
     * given input dictionary, with given inputs fileName and cacheSize.
        - Parameters:
            - fileName:   the file to read the finite state machine.
            - dictionary: the dictionary file that will be used to generate dictionaryTrie.
            - cacheSize:  the size of the LRUCache.
     */
    public init(fileName: String, dictionary: TxtDictionary, cacheSize: Int){
        self.dictionary = dictionary;
        finiteStateMachine = FiniteStateMachine(fileName: fileName)
        dictionaryTrie = dictionary.prepareTrie()
        if cacheSize > 0{
            cache = LRUCache(cacheSize: cacheSize)
        } else {
            cache = nil
        }
    }
    
    /**
     * Another constructor of FsmMorphologicalAnalyzer class. It generates a new TxtDictionary type dictionary from
     * given input dictionary, with given input fileName and fixed size cacheSize = 10000000.
        - Parameters:
            - fileName:   the file to read the finite state machine.
            - dictionary: the dictionary file that will be used to generate dictionaryTrie.
     */
    public convenience init(fileName: String, dictionary: TxtDictionary){
        self.init(fileName: fileName, dictionary: dictionary, cacheSize: 10000000)
    }
    
    /**
     * Another constructor of FsmMorphologicalAnalyzer class. It generates a new TxtDictionary type dictionary from
     * given input dictionary, with given input fileName and fixed size cacheSize = 10000000.
        - Parameters:
            - dictionary: the dictionary file that will be used to generate dictionaryTrie.
     */
    public convenience init(dictionary: TxtDictionary){
        self.init(fileName: "turkish_finite_state_machine", dictionary: dictionary, cacheSize: 10000000)
    }
    
    /// Reads the file for correct surface forms and their most frequent root forms, in other words, the surface forms
    /// which have at least one morphological analysis in  Turkish.
    /// - Parameter fileName: Input file containing analyzable surface forms and their root forms.
    public func addParsedSurfaceForms(fileName: String){
        parsedSurfaceForms = []
        let thisSourceFile = URL(fileURLWithPath: #file)
        let thisDirectory = thisSourceFile.deletingLastPathComponent()
        let url = thisDirectory.appendingPathComponent(fileName)
        do{
            let fileContent = try String(contentsOf: url, encoding: .utf8)
            let lines : [String] = fileContent.split(whereSeparator: \.isNewline).map(String.init)
            for line in lines{
                parsedSurfaceForms?.insert(line)
            }
        }catch{
        }
    }
    
    /**
     * The getPossibleWords method takes {@link MorphologicalParse} and {@link MetamorphicParse} as input.
     * First it determines whether the given morphologicalParse is the root verb and whether it contains a verb tag.
     * Then it creates new transition with -mak and creates a new {@link HashSet} result.
     * <p>
     * It takes the given {@link MetamorphicParse} input as currentWord and if there is a compound word starting with the
     * currentWord, it gets this compoundWord from dictionaryTrie. If there is a compoundWord and the difference of the
     * currentWord and compundWords is less than 3 than compoundWord is added to the result, otherwise currentWord is added.
     * <p>
     * Then it gets the root from parse input as a currentRoot. If it is not null, and morphologicalParse input is verb,
     * it directly adds the verb to result after making transition to currentRoot with currentWord String. Else, it creates a new
     * transition with -lar and make this transition then adds to the result.
        - Parameters:
            - morphologicalParse: {@link MorphologicalParse} type input.
            - metamorphicParse:             {@link MetamorphicParse} type input.
        - Returns: {@link HashSet} result.
     */
    public func getPossibleWords(morphologicalParse: MorphologicalParse, metamorphicParse: MetamorphicParse) -> Set<String>{
        let isRootVerb : Bool = morphologicalParse.getRootPos() == "VERB"
        let containsVerb : Bool = morphologicalParse.containsTag(tag: MorphologicalTag.VERB)
        var transition : Transition
        let verbTransition : Transition = Transition(with: "mAk")
        var compoundWord, currentRoot : TxtWord?
        var result : Set<String> = []
        var verbWord : String
        var pluralWord : String?
        var currentWord : String = metamorphicParse.getWord().getName()
        var pluralIndex : Int = -1
        compoundWord = dictionaryTrie.getCompoundWordStartingWith(_hash: currentWord)
        if !isRootVerb {
            if compoundWord != nil && compoundWord!.getName().count - currentWord.count < 3 {
                result.insert(compoundWord!.getName())
            }
            result.insert(currentWord)
        }
        currentRoot = dictionary.getWord(name: metamorphicParse.getWord().getName()) as? TxtWord
        if (currentRoot == nil && compoundWord != nil) {
            currentRoot = compoundWord
        }
        if currentRoot != nil {
            if isRootVerb {
                verbWord = verbTransition.makeTransition(root: currentRoot!, stem: currentWord);
                result.insert(verbWord)
            }
            pluralWord = nil
            for i in 1 ..< metamorphicParse.size() {
                transition = Transition(toState: nil, with: metamorphicParse.getMetaMorpheme(index: i), withName: nil)
                if metamorphicParse.getMetaMorpheme(index: i) == "lAr" {
                    pluralWord = currentWord
                    pluralIndex = i + 1
                }
                currentWord = transition.makeTransition(root: currentRoot!, stem: currentWord)
                result.insert(currentWord)
                if containsVerb {
                    verbWord = verbTransition.makeTransition(root: currentRoot!, stem: currentWord)
                    result.insert(verbWord)
                }
            }
            if pluralWord != nil {
                currentWord = pluralWord!
                for i in pluralIndex..<metamorphicParse.size() {
                    transition = Transition(toState: nil, with: metamorphicParse.getMetaMorpheme(index: i), withName: nil)
                    currentWord = transition.makeTransition(root: currentRoot!, stem: currentWord)
                    result.insert(currentWord)
                    if containsVerb {
                        verbWord = verbTransition.makeTransition(root: currentRoot!, stem: currentWord)
                        result.insert(verbWord)
                    }
                }
            }
        }
        return result
    }
    
    /**
     * The getDictionary method is used to get TxtDictionary.
     *
        - Returns: TxtDictionary type dictionary.
     */
    public func getDictionary() -> TxtDictionary{
        return dictionary
    }
    
    /**
     * The getFiniteStateMachine method is used to get FiniteStateMachine.
     *
        - Returns: FiniteStateMachine type finiteStateMachine.
     */
    public func getFiniteStateMachine() -> FiniteStateMachine{
        return finiteStateMachine
    }
    
    /**
     * The isPossibleSubstring method first checks whether given short and long strings are equal to root word.
     * Then, compares both short and long strings' chars till the last two chars of short string. In the presence of mismatch,
     * false is returned. On the other hand, it counts the distance between two strings until it becomes greater than 2,
     * which is the MAX_DISTANCE also finds the index of the last char.
     * <p>
     * If the substring is a rootWord and equals to 'ben', which is a special case or root holds the lastIdropsDuringSuffixation or
     * lastIdropsDuringPassiveSuffixation conditions, then it returns true if distance is not greater than MAX_DISTANCE.
     * <p>
     * On the other hand, if the shortStrong ends with one of these chars 'e, a, p, ç, t, k' and 't 's a rootWord with
     * the conditions of rootSoftenDuringSuffixation, vowelEChangesToIDuringYSuffixation, vowelAChangesToIDuringYSuffixation
     * or endingKChangesIntoG then it returns true if the last index is not equal to 2 and distance is not greater than
     * MAX_DISTANCE and false otherwise.
        - Parameters:
            - shortString: the possible substring.
            - longString:  the long string to compare with substring.
            - root:        the root of the long string.
        - Returns: true if given substring is the actual substring of the longString, false otherwise.
     */
    public func isPossibleSubstring(shortString: String, longString: String, root: TxtWord) -> Bool{
        let rootWord : Bool = ((shortString == root.getName()) || longString == root.getName())
        var distance : Int = 0
        var last : Int = 1
        for j in 0..<shortString.count {
            if Word.charAt(s: shortString, i: j) != Word.charAt(s: longString, i: j) {
                if j < shortString.count - 2 {
                    return false
                }
                last = shortString.count - j
                distance += 1
                if distance > FsmMorphologicalAnalyzer.MAX_DISTANCE {
                    break
                }
            }
        }
        if rootWord && (root.getName() == "ben" || root.getName() == "sen" || root.lastIdropsDuringSuffixation() || root.lastIdropsDuringPassiveSuffixation()) {
            return distance <= FsmMorphologicalAnalyzer.MAX_DISTANCE
        } else {
            if shortString.hasSuffix("e") || shortString.hasSuffix("a") || shortString.hasSuffix("p") || shortString.hasSuffix("ç") || shortString.hasSuffix("t") || shortString.hasSuffix("k") || (rootWord && (root.rootSoftenDuringSuffixation() || root.vowelEChangesToIDuringYSuffixation() || root.vowelAChangesToIDuringYSuffixation() || root.endingKChangesIntoG())) {
                return last != 2 && distance <= FsmMorphologicalAnalyzer.MAX_DISTANCE - 1
            } else {
                return distance <= FsmMorphologicalAnalyzer.MAX_DISTANCE - 2
            }
        }
    }
    
    /**
     * The initializeParseList method initializes the given given fsm ArrayList with given root words by parsing them.
     * <p>
     * It checks many conditions;
     * isPlural; if root holds the condition then it gets the state with the name of NominalRootPlural, then
     * creates a new parsing and adds this to the input fsmParse Arraylist.
     * Ex : Açıktohumlular
     * <p>
     * !isPlural and isPortmanteauEndingWithSI, if root holds the conditions then it gets the state with the
     * name of NominalRootNoPossesive.
     * Ex : Balarısı
     * <p>
     * !isPlural and isPortmanteau, if root holds the conditions then it gets the state with the name of
     * CompoundNounRoot.
     * Ex : Aslanağızı
     * <p>
     * !isPlural, !isPortmanteau and isHeader, if root holds the conditions then it gets the state with the
     * name of HeaderRoot.
     * Ex :  </title>
     * <p>
     * !isPlural, !isPortmanteau and isInterjection, if root holds the conditions then it gets the state
     * with the name of InterjectionRoot.
     * Ex : Hey, Aa
     * <p>
     * !isPlural, !isPortmanteau and isDuplicate, if root holds the conditions then it gets the state
     * with the name of DuplicateRoot.
     * Ex : Allak,
     * <p>
     * !isPlural, !isPortmanteau and isCode, if root holds the conditions then it gets the state
     * with the name of CodeRoot.
     * Ex : 9400f,
     * <p>
     * !isPlural, !isPortmanteau and isMetric, if root holds the conditions then it gets the state
     * with the name of MetricRoot.
     * Ex : 11x8x12,
     * <p>
     * !isPlural, !isPortmanteau and isNumeral, if root holds the conditions then it gets the state
     * with the name of CardinalRoot.
     * Ex : Yüz, bin
     * <p>
     * !isPlural, !isPortmanteau and isReal, if root holds the conditions then it gets the state
     * with the name of RealRoot.
     * Ex : 1.2
     * <p>
     * !isPlural, !isPortmanteau and isFraction, if root holds the conditions then it gets the state
     * with the name of FractionRoot.
     * Ex : 1/2
     * <p>
     * !isPlural, !isPortmanteau and isDate, if root holds the conditions then it gets the state
     * with the name of DateRoot.
     * Ex : 11/06/2018
     * <p>
     * !isPlural, !isPortmanteau and isPercent, if root holds the conditions then it gets the state
     * with the name of PercentRoot.
     * Ex : %12.5
     * <p>
     * !isPlural, !isPortmanteau and isRange, if root holds the conditions then it gets the state
     * with the name of RangeRoot.
     * Ex : 3-5
     * <p>
     * !isPlural, !isPortmanteau and isTime, if root holds the conditions then it gets the state
     * with the name of TimeRoot.
     * Ex : 13:16:08
     * <p>
     * !isPlural, !isPortmanteau and isOrdinal, if root holds the conditions then it gets the state
     * with the name of OrdinalRoot.
     * Ex : Altıncı
     * <p>
     * !isPlural, !isPortmanteau, and isVerb if root holds the conditions then it gets the state
     * with the name of VerbalRoot. Or isPassive, then it gets the state with the name of PassiveHn.
     * Ex : Anla (!isPAssive)
     * Ex : Çağrıl (isPassive)
     * <p>
     * !isPlural, !isPortmanteau and isPronoun, if root holds the conditions then it gets the state
     * with the name of PronounRoot. There are 6 different Pronoun state names, REFLEX, QUANT, QUANTPLURAL, DEMONS, PERS, QUES.
     * REFLEX = Reflexive Pronouns Ex : kendi
     * QUANT = Quantitative Pronouns Ex : öbür, hep, kimse, hiçbiri, bazı, kimi, biri
     * QUANTPLURAL = Quantitative Plural Pronouns Ex : tümü, çoğu, hepsi
     * DEMONS = Demonstrative Pronouns Ex : o, bu, şu
     * PERS = Personal Pronouns Ex : ben, sen, o, biz, siz, onlar
     * QUES = Interrogatıve Pronouns Ex : nere, ne, kim, hangi
     * <p>
     * !isPlural, !isPortmanteau and isAdjective, if root holds the conditions then it gets the state
     * with the name of AdjectiveRoot.
     * Ex : Absürt, Abes
     * <p>
     * !isPlural, !isPortmanteau and isPureAdjective, if root holds the conditions then it gets the state
     * with the name of Adjective.
     * Ex : Geçmiş, Cam
     * <p>
     * !isPlural, !isPortmanteau and isNominal, if root holds the conditions then it gets the state
     * with the name of NominalRoot.
     * Ex : Görüş
     * <p>
     * !isPlural, !isPortmanteau and isProper, if root holds the conditions then it gets the state
     * with the name of ProperRoot.
     * Ex : Abdi
     * <p>
     * !isPlural, !isPortmanteau and isQuestion, if root holds the conditions then it gets the state
     * with the name of QuestionRoot.
     * Ex : Mi, mü
     * <p>
     * !isPlural, !isPortmanteau and isDeterminer, if root holds the conditions then it gets the state
     * with the name of DeterminerRoot.
     * Ex : Çok, bir
     * <p>
     * !isPlural, !isPortmanteau and isConjunction, if root holds the conditions then it gets the state
     * with the name of ConjunctionRoot.
     * Ex : Ama , ancak
     * <p>
     * !isPlural, !isPortmanteau and isPostP, if root holds the conditions then it gets the state
     * with the name of PostP.
     * Ex : Ait, dair
     * <p>
     * !isPlural, !isPortmanteau and isAdverb, if root holds the conditions then it gets the state
     * with the name of AdverbRoot.
     * Ex : Acilen
        - Parameters:
            - fsmParse: ArrayList to initialize.
            - root:     word to check properties and add to fsmParse according to them.
            - isProper: is used to check a word is proper or not.
     */
    private func initializeParseList(fsmParse: inout [FsmParse], root: TxtWord, isProper: Bool){
        var currentFsmParse : FsmParse
        if root.isPlural() {
            currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "NominalRootPlural")!)
            fsmParse.append(currentFsmParse)
        } else {
            if root.isPortmanteauEndingWithSI() {
                currentFsmParse = FsmParse(punctuation: root.getName().prefix(root.getName().count - 2) + "", startState: finiteStateMachine.getState(name: "CompoundNounRoot")!)
                fsmParse.append(currentFsmParse);
                currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "NominalRootNoPossesive")!)
                fsmParse.append(currentFsmParse)
            } else {
                if root.isPortmanteau() {
                    if root.isPortmanteauFacedVowelEllipsis() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "NominalRootNoPossesive")!)
                        fsmParse.append(currentFsmParse)
                        currentFsmParse = FsmParse(punctuation: root.getName().prefix(root.getName().count - 2) + String(Word.charAt(s: root.getName(), i: root.getName().count - 1)) + String(Word.charAt(s: root.getName(), i: root.getName().count - 2)), startState: finiteStateMachine.getState(name: "CompoundNounRoot")!)
                    } else {
                        if root.isPortmanteauFacedSoftening() {
                            currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "NominalRootNoPossesive")!)
                            fsmParse.append(currentFsmParse)
                            switch Word.charAt(s: root.getName(), i: root.getName().count - 2){
                                case "b":
                                    currentFsmParse = FsmParse(punctuation: root.getName().prefix(root.getName().count - 2) + "p", startState: finiteStateMachine.getState(name: "CompoundNounRoot")!)
                                    break
                                case "c":
                                    currentFsmParse = FsmParse(punctuation: root.getName().prefix(root.getName().count - 2) + "ç", startState: finiteStateMachine.getState(name: "CompoundNounRoot")!)
                                    break
                                case "d":
                                    currentFsmParse = FsmParse(punctuation: root.getName().prefix(root.getName().count - 2) + "t", startState: finiteStateMachine.getState(name: "CompoundNounRoot")!)
                                    break
                                case "ğ":
                                    currentFsmParse = FsmParse(punctuation: root.getName().prefix(root.getName().count - 2) + "k", startState: finiteStateMachine.getState(name: "CompoundNounRoot")!)
                                    break
                                default:
                                    currentFsmParse = FsmParse(punctuation: root.getName().prefix(root.getName().count - 1) + "", startState: finiteStateMachine.getState(name: "CompoundNounRoot")!)
                            }
                        } else {
                            currentFsmParse = FsmParse(punctuation: root.getName().prefix(root.getName().count - 1) + "", startState: finiteStateMachine.getState(name: "CompoundNounRoot")!)
                        }
                    }
                    fsmParse.append(currentFsmParse)
                } else {
                    if root.isHeader() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "HeaderRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isInterjection() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "InterjectionRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isDuplicate() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "DuplicateRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isCode() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "CodeRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isMetric(){
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "MetricRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isNumeral() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "CardinalRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isReal() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "RealRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isFraction() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "FractionRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isDate() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "DateRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isPercent() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "PercentRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isRange() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "RangeRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isTime() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "TimeRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isOrdinal() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "OrdinalRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isVerb() || root.isPassive() {
                        if root.verbType() != "" {
                            currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "VerbalRoot(" + root.verbType() + ")")!)
                        } else {
                            if !root.isPassive() {
                                currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "VerbalRoot")!)
                            } else {
                                currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "PassiveHn")!)
                            }
                        }
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isPronoun() {
                        if root.getName() == "kendi" {
                            currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "PronounRoot(REFLEX)")!)
                            fsmParse.append(currentFsmParse)
                        }
                        if root.getName() == "öbür" || root.getName() == "öteki" || root.getName() == "hep" || root.getName() == "kimse" || root.getName() == "diğeri" || root.getName() == "hiçbiri" || root.getName() == "böylesi" || root.getName() == "birbiri" || root.getName() == "birbirleri" || root.getName() == "biri" || root.getName() == "başkası" || root.getName() == "bazı" || root.getName() == "kimi" {
                            currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "PronounRoot(QUANT)")!)
                            fsmParse.append(currentFsmParse)
                        }
                        if root.getName() == "tümü" || root.getName() == "topu" || root.getName() == "herkes" || root.getName() == "cümlesi" || root.getName() == "çoğu" || root.getName() == "birçoğu" || root.getName() == "birkaçı" || root.getName() == "birçokları" || root.getName() == "hepsi" {
                            currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "PronounRoot(QUANTPLURAL)")!)
                            fsmParse.append(currentFsmParse)
                        }
                        if root.getName() == "o" || root.getName() == "bu" || root.getName() == "şu" {
                            currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "PronounRoot(DEMONS)")!)
                            fsmParse.append(currentFsmParse)
                        }
                        if root.getName() == "ben" || root.getName() == "sen" || root.getName() == "o" || root.getName() == "biz" || root.getName() == "siz" || root.getName() == "onlar" {
                            currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "PronounRoot(PERS)")!)
                            fsmParse.append(currentFsmParse)
                        }
                        if root.getName() == "nere" || root.getName() == "ne" || root.getName() == "kaçı" || root.getName() == "kim" || root.getName() == "hangi" {
                            currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "PronounRoot(QUES)")!)
                            fsmParse.append(currentFsmParse)
                        }
                    }
                    if root.isAdjective() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "AdjectiveRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isPureAdjective() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "Adjective")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isNominal() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "NominalRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isAbbreviation() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "NominalRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isProperNoun() && isProper {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "ProperRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isQuestion() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "QuestionRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isDeterminer() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "DeterminerRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isConjunction() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "ConjunctionRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isPostP() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "PostP")!)
                        fsmParse.append(currentFsmParse)
                    }
                    if root.isAdverb() {
                        currentFsmParse = FsmParse(root: root, startState: finiteStateMachine.getState(name: "AdverbRoot")!)
                        fsmParse.append(currentFsmParse)
                    }
                }
            }
        }
    }
    
    /**
     * The initializeParseListFromRoot method is used to create an {@link ArrayList} which consists of initial fsm parsings. First, traverses
     * this HashSet and uses each word as a root and calls initializeParseList method with this root and ArrayList.
     * <p>
        - Parameters:
            - parseList: ArrayList to initialize.
            - root: the root form to generate initial parse list.
            - isProper: is used to check a word is proper or not.
     */
    private func initializeParseListFromRoot(parseList: inout [FsmParse], root: TxtWord, isProper: Bool){
        initializeParseList(fsmParse: &parseList, root: root, isProper: isProper)
        if root.obeysAndNotObeysVowelHarmonyDuringAgglutination(){
            let newRoot : TxtWord = root.copy() as! TxtWord
            newRoot.removeFlag(flag: "IS_UU")
            newRoot.removeFlag(flag: "IS_UUU")
            initializeParseList(fsmParse: &parseList, root: newRoot, isProper: isProper)
        }
        if root.rootSoftenAndNotSoftenDuringSuffixation() {
            let newRoot : TxtWord = root.copy() as! TxtWord
            newRoot.removeFlag(flag: "IS_SD")
            newRoot.removeFlag(flag: "IS_SDD")
            initializeParseList(fsmParse: &parseList, root: newRoot, isProper: isProper)
        }
        if (root.lastIDropsAndNotDropDuringSuffixation()){
            let newRoot : TxtWord = root.copy() as! TxtWord
            newRoot.removeFlag(flag: "IS_UD")
            newRoot.removeFlag(flag: "IS_UDD")
            initializeParseList(fsmParse: &parseList, root: newRoot, isProper: isProper)
        }
        if (root.duplicatesAndNotDuplicatesDuringSuffixation()){
            let newRoot : TxtWord = root.copy() as! TxtWord
            newRoot.removeFlag(flag: "IS_ST")
            newRoot.removeFlag(flag: "IS_STT")
            initializeParseList(fsmParse: &parseList, root: newRoot, isProper: isProper)
        }
        if (root.endingKChangesIntoG() && root.containsFlag(flag: "IS_OA")){
            let newRoot : TxtWord = root.copy() as! TxtWord
            newRoot.removeFlag(flag: "IS_OA")
            initializeParseList(fsmParse: &parseList, root: newRoot, isProper: isProper)
        }
    }
    
    /**
     * The initializeParseListFromSurfaceForm method is used to create an {@link ArrayList} which consists of initial fsm parsings. First,
     * it calls getWordsWithPrefix methods by using input String surfaceForm and generates a {@link HashSet}. Then, traverses
     * this HashSet and uses each word as a root and calls initializeParseListFromRoot method with this root and ArrayList.
     * <p>
        - Parameters:
            - surfaceForm: the String used to generate a HashSet of words.
            - isProper :   is used to check a word is proper or not.
        - Returns: initialFsmParse ArrayList.
     */
    private func initializeParseListFromSurfaceForm(surfaceForm: String, isProper: Bool) -> [FsmParse]{
        var root : TxtWord
        var initialFsmParse : [FsmParse] = []
        if surfaceForm.count == 0 {
            return initialFsmParse
        }
        let words : Set<Word> = dictionaryTrie.getWordsWithPrefix(surfaceForm: surfaceForm)
        for word in words {
            root = word as! TxtWord
            initializeParseListFromRoot(parseList: &initialFsmParse, root: root, isProper: isProper)
        }
        return initialFsmParse
    }
    
    /**
     * The addNewParsesFromCurrentParse method initially gets the final suffixes from input currentFsmParse called as currentState,
     * and by using the currentState information it gets the new analysis. Then loops through each currentState's transition.
     * If the currentTransition is possible, it makes the transition.
        - Parameters:
            - currentFsmParse: FsmParse type input.
            - fsmParse:        an ArrayList of FsmParse.
            - maxLength:     Maximum length of the parse.
            - root :           TxtWord used to make transition.
     */
    private func addNewParsesFromCurrentParse(currentFsmParse: FsmParse, fsmParse: inout [FsmParse], maxLength: Int,  root: TxtWord){
        let currentState : FsmState = currentFsmParse.getFinalSuffix()
        let currentSurfaceForm : String = currentFsmParse.getSurfaceForm()
        for currentTransition in finiteStateMachine.getTransitions(state: currentState) {
            if currentTransition.transitionPossible(currentFsmParse: currentFsmParse) && (currentSurfaceForm != root.getName() || (currentSurfaceForm == root.getName() && currentTransition.transitionPossible(root: root, fromState: currentState))) {
                let tmp : String = currentTransition.makeTransition(root: root, stem: currentSurfaceForm, startState: currentFsmParse.getStartState())
                if tmp.count <= maxLength {
                    let newFsmParse : FsmParse = currentFsmParse.copy() as! FsmParse
                    newFsmParse.addSuffix(suffix: currentTransition.getToState()!, form: tmp, transition: currentTransition.with(), with: currentTransition.description(), toPos: currentTransition.toPos())
                    newFsmParse.setAgreement(transitionName: currentTransition.with())
                    fsmParse.append(newFsmParse)
                }
            }
        }
    }
    
    /**
     * The addNewParsesFromCurrentParse method initially gets the final suffixes from input currentFsmParse called as currentState,
     * and by using the currentState information it gets the currentSurfaceForm. Then loops through each currentState's transition.
     * If the currentTransition is possible, it makes the transition
        - Parameters:
            - currentFsmParse: FsmParse type input.
            - fsmParse:        an ArrayList of FsmParse.
            - surfaceForm :    String to use during transition.
            - root :           TxtWord used to make transition.
     */
    private func addNewParsesFromCurrentParse(currentFsmParse: FsmParse, fsmParse: inout [FsmParse], surfaceForm: String, root: TxtWord){
        let currentState : FsmState = currentFsmParse.getFinalSuffix()
        let currentSurfaceForm : String = currentFsmParse.getSurfaceForm()
        for currentTransition in finiteStateMachine.getTransitions(state: currentState) {
            if currentTransition.transitionPossible(currentSurfaceForm: currentFsmParse.getSurfaceForm(), realSurfaceForm: surfaceForm) && currentTransition.transitionPossible(currentFsmParse: currentFsmParse) && (currentSurfaceForm != root.getName() || (currentSurfaceForm == root.getName() && currentTransition.transitionPossible(root: root, fromState: currentState))) {
                let tmp : String = currentTransition.makeTransition(root: root, stem: currentSurfaceForm, startState: currentFsmParse.getStartState())
                if (tmp.count < surfaceForm.count && isPossibleSubstring(shortString: tmp, longString: surfaceForm, root: root)) || (tmp.count == surfaceForm.count && (root.lastIdropsDuringSuffixation() || tmp == surfaceForm)) {
                    let newFsmParse : FsmParse = currentFsmParse.copy() as! FsmParse
                    newFsmParse.addSuffix(suffix: currentTransition.getToState()!, form: tmp, transition: currentTransition.with(), with: currentTransition.description(), toPos: currentTransition.toPos())
                    newFsmParse.setAgreement(transitionName: currentTransition.with())
                    fsmParse.append(newFsmParse)
                }
            }
        }
    }
    
    /**
     * The parseExists method is used to check the existence of the parse.
        - Parameters:
            - fsmParse:    an ArrayList of FsmParse
            - surfaceForm: String to use during transition.
        - Returns: true when the currentState is end state and input surfaceForm id equal to currentSurfaceForm, otherwise false.
     */
    private func parseExists(fsmParse : inout [FsmParse], surfaceForm: String) -> Bool{
        var currentFsmParse: FsmParse
        var root: TxtWord
        var currentState: FsmState
        var currentSurfaceForm: String
        while fsmParse.count > 0 {
            currentFsmParse = fsmParse.remove(at: 0)
            root = currentFsmParse.getWord() as! TxtWord
            currentState = currentFsmParse.getFinalSuffix()
            currentSurfaceForm = currentFsmParse.getSurfaceForm()
            if currentState.isEndState() && currentSurfaceForm == surfaceForm {
                return true
            }
            addNewParsesFromCurrentParse(currentFsmParse: currentFsmParse, fsmParse: &fsmParse, surfaceForm: surfaceForm, root: root)
        }
        return false
    }
    
    /**
     * The parseWord method is used to parse a given fsmParse. It simply adds new parses to the current parse by
     * using addNewParsesFromCurrentParse method.
        - Parameters:
            - fsmParse:    an ArrayList of FsmParse
            - maxLength: maximum length of the surfaceform.
        - Returns: result {@link ArrayList} which has the currentFsmParse.
     */
    private func parseWord(fsmParse: inout [FsmParse], maxLength: Int) -> [FsmParse]{
        var result : [FsmParse] = []
        var resultSuffixList : [String] = []
        var currentFsmParse : FsmParse
        var root : TxtWord
        var currentState: FsmState
        var currentSurfaceForm: String
        var currentSuffixList: String
        while fsmParse.count > 0 {
            currentFsmParse = fsmParse.remove(at: 0)
            root = currentFsmParse.getWord() as! TxtWord
            currentState = currentFsmParse.getFinalSuffix()
            currentSurfaceForm = currentFsmParse.getSurfaceForm()
            if currentState.isEndState() && currentSurfaceForm.count <= maxLength {
                currentSuffixList = currentFsmParse.suffixList()
                if !resultSuffixList.contains(currentSuffixList) {
                    result.append(currentFsmParse)
                    currentFsmParse.constructInflectionalGroups()
                    resultSuffixList.append(currentSuffixList)
                }
            }
            addNewParsesFromCurrentParse(currentFsmParse: currentFsmParse, fsmParse: &fsmParse, maxLength: maxLength, root: root)
        }
        return result
    }
    
    /**
     * The parseWord method is used to parse a given fsmParse. It simply adds new parses to the current parse by
     * using addNewParsesFromCurrentParse method.
        - Parameters:
            - fsmParse:    an ArrayList of FsmParse
            - surfaceForm: String to use during transition.
        - Returns: result {@link ArrayList} which has the currentFsmParse.
     */
    private func parseWord(fsmParse: inout [FsmParse], surfaceForm: String) -> [FsmParse] {
        var result : [FsmParse] = []
        var resultSuffixList : [String] = []
        var currentFsmParse : FsmParse
        var root : TxtWord
        var currentState: FsmState
        var currentSurfaceForm: String
        var currentSuffixList: String
        while fsmParse.count > 0 {
            currentFsmParse = fsmParse.remove(at: 0)
            root = currentFsmParse.getWord() as! TxtWord
            currentState = currentFsmParse.getFinalSuffix()
            currentSurfaceForm = currentFsmParse.getSurfaceForm()
            if currentState.isEndState() && currentSurfaceForm == surfaceForm {
                currentSuffixList = currentFsmParse.suffixList()
                if !resultSuffixList.contains(currentSuffixList) {
                    result.append(currentFsmParse)
                    currentFsmParse.constructInflectionalGroups()
                    resultSuffixList.append(currentSuffixList)
                }
            }
            addNewParsesFromCurrentParse(currentFsmParse: currentFsmParse, fsmParse: &fsmParse, surfaceForm: surfaceForm, root: root)
        }
        return result
    }
    
    /**
     * The morphologicalAnalysis with 3 inputs is used to initialize an {@link ArrayList} and add a new FsmParse
     * with given root and state.
        - Parameters:
            - root:        TxtWord input.
            - surfaceForm: String input to use for parsing.
            - state:       String input.
        - Returns: parseWord method with newly populated FsmParse ArrayList and input surfaceForm.
     */
    public func morphologicalAnalysis(root: TxtWord, surfaceForm: String, state: String) -> [FsmParse]{
        var initialFsmParse : [FsmParse] = []
        initialFsmParse.append(FsmParse(root: root, startState: finiteStateMachine.getState(name: state)!))
        return parseWord(fsmParse: &initialFsmParse, surfaceForm: surfaceForm)
    }
    
    /// Given a set of morphological parses, this method returns all surface forms of those parses.
    /// - Parameter parseList: Morphological parse list.
    /// - Returns: All distinct surface forms for a given set of morphological parses.
    public func distinctSurfaceFormList(parseList: [FsmParse]) -> Set<String>{
        var items: Set<String> = []
        for parse in parseList {
            items.insert(parse.getSurfaceForm())
        }
        return items
    }
    
    /**
     * The generateAllParses with 2 inputs is used to generate all parses with given root. Then it calls initializeParseListFromRoot method to initialize list with newly created ArrayList, input root,
     * and maximum length.
        - Parameters:
            - root:        TxtWord input.
            - maxLength: Maximum length of the surface form.
        - Returns: parseWord method with newly populated FsmParse ArrayList and maximum length.
     */
    public func generateAllParses(root: TxtWord, maxLength: Int) -> [FsmParse]{
        var initialFsmParse : [FsmParse] = []
        if root.isProperNoun() {
            initializeParseListFromRoot(parseList: &initialFsmParse, root: root, isProper: true)
        }
        initializeParseListFromRoot(parseList: &initialFsmParse, root: root, isProper: false)
        return parseWord(fsmParse: &initialFsmParse, maxLength: maxLength)
    }
    
    /**
     * The morphologicalAnalysis with 2 inputs is used to initialize an {@link ArrayList} and add a new FsmParse
     * with given root. Then it calls initializeParseListFromRoot method to initialize list with newly created ArrayList, input root,
     * and input surfaceForm.
        - Parameters:
            - root:        TxtWord input.
            - surfaceForm: String input to use for parsing.
        - Returns: parseWord method with newly populated FsmParse ArrayList and input surfaceForm.
     */
    public func morphologicalAnalysis(root: TxtWord, surfaceForm: String) -> [FsmParse]{
        var initialFsmParse : [FsmParse] = []
        initializeParseListFromRoot(parseList: &initialFsmParse, root: root, isProper: isProperNoun(surfaceForm: surfaceForm))
        return parseWord(fsmParse: &initialFsmParse, surfaceForm: surfaceForm)
    }
    
    /// Replaces previous lemma in the sentence with the new lemma. Both lemma can contain multiple words.
    /// - Parameters:
    ///   - original: Original sentence to be replaced with.
    ///   - previousWord: Root word in the original sentence
    ///   - newWord: newWord New word to be replaced.
    /// - Returns: Newly generated sentence by replacing the previous word in the original sentence with the new word.
    public func replaceWord(original: Sentence, previousWord: String, newWord: String) -> Sentence{
        var i : Int = 0
        var previousWordSplitted : [String] = []
        var newWordSplitted : [String] = []
        let result : Sentence = Sentence()
        var lastWord, newRootWord : String
        let previousWordMultiple : Bool = previousWord.contains(" ")
        let newWordMultiple : Bool = newWord.contains(" ")
        if previousWordMultiple {
            previousWordSplitted = previousWord.components(separatedBy: " ")
            lastWord = previousWordSplitted[previousWordSplitted.count - 1]
        } else {
            lastWord = previousWord
        }
        if (newWordMultiple){
            newWordSplitted = newWord.components(separatedBy: " ")
            newRootWord = newWordSplitted[newWordSplitted.count - 1]
        } else {
            newRootWord = newWord
        }
        let newRootTxtWord = dictionary.getWord(name: newRootWord)
        let parseList = morphologicalAnalysis(sentence: original)
        while i < parseList.count {
            var replaced = false
            var replacedWord : String = ""
            for j in 0..<parseList[i].size() {
                if parseList[i].getFsmParse(index: j).root.getName() == lastWord && newRootTxtWord != nil {
                    replaced = true
                    replacedWord = parseList[i].getFsmParse(index: j).replaceRootWord(newRoot: newRootTxtWord as! TxtWord)
                }
            }
            if replaced {
                if previousWordMultiple{
                    for k in 0..<i - previousWordSplitted.count + 1{
                        result.addWord(word: original.getWord(index: k))
                    }
                }
                if newWordMultiple{
                    for k in 0..<newWordSplitted.count - 1 {
                        result.addWord(word: Word(name: newWordSplitted[k]))
                    }
                }
                result.addWord(word: Word(name: replacedWord))
                if previousWordMultiple{
                    i = i + 1
                    break;
                }
            } else {
                if !previousWordMultiple{
                    result.addWord(word: original.getWord(index: i))
                }
            }
            i = i + 1
        }
        if previousWordMultiple{
            while i < parseList.count {
                result.addWord(word: original.getWord(index: i))
                i = i + 1
            }
        }
        return result
    }
    
    /**
     * The analysisExists method checks several cases. If the given surfaceForm is a punctuation or double then it
     * returns true. If it is not a root word, then it initializes the parse list and returns the parseExists method with
     * this newly initialized list and surfaceForm.
        - Parameters:
            - rootWord:    TxtWord root.
            - surfaceForm: String input.
            - isProper:    boolean variable indicates a word is proper or not.
        - Returns: true if surfaceForm is punctuation or double, otherwise returns parseExist method with given surfaceForm.
     */
    private func analysisExists(rootWord: TxtWord?, surfaceForm: String, isProper: Bool) -> Bool{
        var initialFsmParse : [FsmParse]
        if Word.isPunctuationSymbol(surfaceForm: surfaceForm) {
            return true
        }
        if isDouble(surfaceForm: surfaceForm) {
            return true
        }
        if rootWord != nil {
            initialFsmParse = []
            initializeParseListFromRoot(parseList: &initialFsmParse, root: rootWord!, isProper: isProper)
        } else {
            initialFsmParse = initializeParseListFromSurfaceForm(surfaceForm: surfaceForm, isProper: isProper)
        }
        return parseExists(fsmParse: &initialFsmParse, surfaceForm: surfaceForm)
    }
    
    /**
     * The analysis method is used by the morphologicalAnalysis method. It gets String surfaceForm as an input and checks
     * its type such as punctuation, number or compares with the regex for date, fraction, percent, time, range, hashtag,
     * and mail or checks its variable type as integer or double. After finding the right case for given surfaceForm, it calls
     * constructInflectionalGroups method which creates sub-word units.
        - Parameters:
            - surfaceForm: String to analyse.
            - isProper:    is used to indicate the proper words.
        - Returns: ArrayList type initialFsmParse which holds the analyses.
     */
    private func analysis(surfaceForm: String, isProper: Bool) -> [FsmParse] {
        var initialFsmParse : [FsmParse]
        var fsmParse : FsmParse
        if Word.isPunctuationSymbol(surfaceForm: surfaceForm) && surfaceForm != "%" {
            initialFsmParse = []
            fsmParse = FsmParse(punctuation: surfaceForm, startState: FsmState(name: ("Punctuation"), startState: true, endState: true))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if isNumber(surfaceForm: surfaceForm) {
            initialFsmParse = []
            fsmParse = FsmParse(punctuation: surfaceForm, startState: FsmState(name: ("CardinalRoot"), startState: true, endState: true))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if patternMatches(expr: "\\d+/\\d+", value: surfaceForm) {
            initialFsmParse = []
            fsmParse = FsmParse(punctuation: surfaceForm, startState: FsmState(name: ("FractionRoot"), startState: true, endState: true))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            fsmParse = FsmParse(punctuation: surfaceForm, startState: FsmState(name: ("DateRoot"), startState: true, endState: true))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if isDate(surfaceForm: surfaceForm) {
            initialFsmParse = []
            fsmParse = FsmParse(punctuation: surfaceForm, startState: FsmState(name: ("DateRoot"), startState: true, endState: true))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if patternMatches(expr: "\\d+\\\\/\\d+", value: surfaceForm) {
            initialFsmParse = []
            fsmParse = FsmParse(punctuation: surfaceForm, startState: FsmState(name: ("FractionRoot"), startState: true, endState: true))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if surfaceForm == "%" || isPercent(surfaceForm: surfaceForm) {
            initialFsmParse = []
            fsmParse = FsmParse(punctuation: surfaceForm, startState: FsmState(name: ("PercentRoot"), startState: true, endState: true))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if isTime(surfaceForm: surfaceForm) {
            initialFsmParse = []
            fsmParse = FsmParse(punctuation: surfaceForm, startState: FsmState(name: ("TimeRoot"), startState: true, endState: true))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if isRange(surfaceForm: surfaceForm) {
            initialFsmParse = []
            fsmParse = FsmParse(punctuation: surfaceForm, startState: FsmState(name: ("RangeRoot"), startState: true, endState: true))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if surfaceForm.hasPrefix("#") {
            initialFsmParse = []
            fsmParse = FsmParse(punctuation: surfaceForm, startState: FsmState(name: ("Hashtag"), startState: true, endState: true))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if surfaceForm.contains("@") {
            initialFsmParse = []
            fsmParse = FsmParse(punctuation: surfaceForm, startState: FsmState(name: ("Email"), startState: true, endState: true))
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if surfaceForm.hasSuffix(".") && isInteger(surfaceForm: String(surfaceForm.prefix(surfaceForm.count - 1))) {
            initialFsmParse = []
            fsmParse = FsmParse(number: Int(String(surfaceForm.prefix(surfaceForm.count - 1)))!, startState: finiteStateMachine.getState(name: "OrdinalRoot")!)
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if isInteger(surfaceForm: surfaceForm) {
            initialFsmParse = []
            fsmParse = FsmParse(number: Int(surfaceForm)!, startState: finiteStateMachine.getState(name: "CardinalRoot")!)
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        if isDouble(surfaceForm: surfaceForm) {
            initialFsmParse = []
            fsmParse = FsmParse(number: Double(surfaceForm)!, startState: finiteStateMachine.getState(name: "RealRoot")!)
            fsmParse.constructInflectionalGroups()
            initialFsmParse.append(fsmParse)
            return initialFsmParse
        }
        initialFsmParse = initializeParseListFromSurfaceForm(surfaceForm: surfaceForm, isProper: isProper)
        return parseWord(fsmParse: &initialFsmParse, surfaceForm: surfaceForm)
    }
    
    /// This method uses cache idea to speed up pattern matching in Fsm. mostUsedPatterns stores the compiled forms of
    /// the previously used patterns. When Fsm tries to match a string to a pattern, first we check if it exists in
    /// mostUsedPatterns. If it exists, we directly use the compiled pattern to match the string. Otherwise, new pattern
    /// is compiled and put in the mostUsedPatterns.
    /// - Parameters:
    ///   - expr: Pattern to check
    ///   - value: String to match the pattern
    /// - Returns: True if the string matches the pattern, false otherwise.
    private func patternMatches(expr: String, value: String) -> Bool{
        var p : NSRegularExpression? = mostUsedPatterns[expr] as? NSRegularExpression
        if p == nil{
            do{
                p = try NSRegularExpression(pattern: expr)
                mostUsedPatterns.setValue(p, forKey: expr)
            } catch {
            }
        }
        let range = NSRange(location: 0, length: value.utf16.count)
        let match = p!.matches(in: value, range: range)
        if match.count == 0{
            return false
        } else {
            return match[0].range.length == range.length
        }
    }
    
    /**
     * The isProperNoun method takes surfaceForm String as input and checks its each char whether they are in the range
     * of letters between A to Z or one of the Turkish letters such as İ, Ü, Ğ, Ş, Ç, and Ö.
        - Parameters:
            - surfaceForm: String to check for proper noun.
        - Returns: false if surfaceForm is null or length of 0, return true if it is a letter.
     */
    public func isProperNoun(surfaceForm: String?) -> Bool{
        if surfaceForm == nil || surfaceForm!.count == 0 {
            return false
        }
        return (Word.charAt(s: surfaceForm!, i: 0) >= "A" && Word.charAt(s: surfaceForm!, i: 0) <= "Z") || Word.charAt(s: surfaceForm!, i: 0) == "İ" || Word.charAt(s: surfaceForm!, i: 0) == "Ü" || Word.charAt(s: surfaceForm!, i: 0) == "Ğ" || Word.charAt(s: surfaceForm!, i: 0) == "Ş" || Word.charAt(s: surfaceForm!, i: 0) == "Ç" || Word.charAt(s: surfaceForm!, i: 0) == "Ö" // İ, Ü, Ğ, Ş, Ç, Ö
    }

    /**
     The isCode method takes surfaceForm String as input and checks if it consists of both letters and numbers
    - parameters:
        - surfaceForm: String to check for code-like word.
    - Returns: true if it is a code-like word, return false otherwise.
     */
    public func isCode(surfaceForm: String?) -> Bool{
        if surfaceForm == nil || surfaceForm!.count == 0 {
            return false
        }
        return patternMatches(expr: ".*[0-9].*", value: surfaceForm!) && patternMatches(expr: ".*[a-zA-ZçöğüşıÇÖĞÜŞİ].*", value: surfaceForm!)
    }
    
    /**
     The robustMorphologicalAnalysis is used to analyse surfaceForm String. First it gets the currentParse of the surfaceForm
     then, if the size of the currentParse is 0, and given surfaceForm is a proper noun, it adds the surfaceForm
     whose state name is ProperRoot to an {@link ArrayList}, of it is not a proper noon, it adds the surfaceForm
     whose state name is NominalRoot to the {@link ArrayList}.
    - Parameters:
        - surfaceForm: String to analyse.
    - Returns: FsmParseList type currentParse which holds morphological analysis of the surfaceForm.
     */
    public func robustMorphologicalAnalysis(surfaceForm: String) -> FsmParseList{
        var fsmParse : [FsmParse]
        var currentParse : FsmParseList
        if surfaceForm == "" {
            return FsmParseList(fsmParses: [])
        }
        currentParse = morphologicalAnalysis(surfaceForm: surfaceForm)
        if currentParse.size() == 0 {
            fsmParse = []
            if isProperNoun(surfaceForm: surfaceForm) {
                fsmParse.append(FsmParse(punctuation: surfaceForm, startState: finiteStateMachine.getState(name: "ProperRoot")!))
            } else {
                if isCode(surfaceForm: surfaceForm) {
                    fsmParse.append(FsmParse(punctuation: surfaceForm, startState: finiteStateMachine.getState(name: "CodeRoot")!))
                } else {
                    fsmParse.append(FsmParse(punctuation: surfaceForm, startState: finiteStateMachine.getState(name: "NominalRoot")!))
                }
            }
            return FsmParseList(fsmParses: parseWord(fsmParse: &fsmParse, surfaceForm: surfaceForm))
        } else {
            return currentParse
        }
    }
    
    /**
     * The morphologicalAnalysis is used for debug purposes.
        - Parameters:
            - sentence:  to get word from.
        - Returns: FsmParseList type result.
     */
    public func morphologicalAnalysis(sentence: Sentence) -> [FsmParseList] {
        var wordFsmParseList : FsmParseList
        var result : [FsmParseList] = []
        for i in 0..<sentence.wordCount() {
            let originalForm : String = sentence.getWord(index: i).getName()
            var spellCorrectedForm : String = dictionary.getCorrectForm(misspelledWord: originalForm)
            if spellCorrectedForm == "" {
                spellCorrectedForm = originalForm
            }
            wordFsmParseList = morphologicalAnalysis(surfaceForm: spellCorrectedForm)
            result.append(wordFsmParseList)
        }
        return result
    }
    
    /**
     * The robustMorphologicalAnalysis method takes just one argument as an input. It gets the name of the words from
     * input sentence then calls robustMorphologicalAnalysis with surfaceForm.
        - Parameters:
            - sentence: Sentence type input used to get surfaceForm.
        - Returns: FsmParseList array which holds the result of the analysis.
     */
    public func robustMorphologicalAnalysis(sentence: Sentence) -> [FsmParseList] {
        var wordFsmParseList : FsmParseList
        var result : [FsmParseList] = []
        for i in 0..<sentence.wordCount() {
            let originalForm : String = sentence.getWord(index: i).getName()
            var spellCorrectedForm : String = dictionary.getCorrectForm(misspelledWord: originalForm)
            if spellCorrectedForm == "" {
                spellCorrectedForm = originalForm
            }
            wordFsmParseList = robustMorphologicalAnalysis(surfaceForm: spellCorrectedForm)
            result.append(wordFsmParseList)
        }
        return result
    }
    
    /**
     * The isInteger method compares input surfaceForm with regex \+?\d+ and returns the result.
     * Supports positive integer checks only.
        - Parameters:
            - surfaceForm: String to check.
        - Returns: true if surfaceForm matches with the regex.
     */
    private func isInteger(surfaceForm: String) -> Bool{
        if !patternMatches(expr: "[+-]?\\d+", value: surfaceForm){
            return false
        }
        let len : Int = surfaceForm.count
        if len < 10 {
            return true
        } else {
            if len > 10 {
                return false
            } else {
                return surfaceForm <= "2147483647"
            }
        }
    }
    
    /**
     * The isDouble method compares input surfaceForm with regex \+?(\d+)?\.\d* and returns the result.
        - Parameters:
            - surfaceForm: String to check.
        - Returns: true if surfaceForm matches with the regex.
     */
    private func isDouble(surfaceForm: String) -> Bool{
        return patternMatches(expr: "[+-]?(\\d+)?\\.\\d*", value: surfaceForm)
    }
    
    /**
     * The isNumber method compares input surfaceForm with the array of written numbers and returns the result.
        - Parameters:
            - surfaceForm: String to check.
        - Returns: true if surfaceForm matches with the regex.
     */
    private func isNumber(surfaceForm: String) -> Bool{
        var found : Bool
        var count : Int = 0
        let numbers : [String] = ["bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz",
                "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan",
                "yüz", "bin", "milyon", "milyar", "trilyon", "katrilyon"]
        var word : String = surfaceForm
        while word != "" {
            found = false
            for number in numbers {
                if word.hasPrefix(number) {
                    found = true
                    count += 1
                    word = String(word.suffix(word.count - number.count))
                    break
                }
            }
            if !found {
                break
            }
        }
        return word == "" && count > 1
    }
    
    /// Checks if a given surface form matches to a percent value. It should be something like %4, %45, %4.3 or %56.786
    /// - Parameter surfaceForm: Surface form to be checked.
    /// - Returns: True if the surface form is in percent form
    private func isPercent(surfaceForm: String) -> Bool{
        return patternMatches(expr: "%(\\d\\d|\\d)", value: surfaceForm) || patternMatches(expr: "%(\\d\\d|\\d)\\.\\d+", value: surfaceForm)
    }
    
    /// Checks if a given surface form matches to a time form. It should be something like 3:34, 12:56 etc.
    /// - Parameter surfaceForm: Surface form to be checked.
    /// - Returns: True if the surface form is in time form
    private func isTime(surfaceForm: String) -> Bool{
        return patternMatches(expr: "(\\d\\d|\\d):(\\d\\d|\\d):(\\d\\d|\\d)", value: surfaceForm) || patternMatches(expr: "(\\d\\d|\\d):(\\d\\d|\\d)", value: surfaceForm)
    }
    
    /// Checks if a given surface form matches to a range form. It should be something like 123-1400 or 12:34-15:78 or
    /// 3.45-4.67.
    /// - Parameter surfaceForm: Surface form to be checked.
    /// - Returns: True if the surface form is in range form
    private func isRange(surfaceForm: String) -> Bool{
        return patternMatches(expr: "\\d+-\\d+", value: surfaceForm) || patternMatches(expr: "(\\d\\d|\\d):(\\d\\d|\\d)-(\\d\\d|\\d):(\\d\\d|\\d)", value: surfaceForm) || patternMatches(expr: "(\\d\\d|\\d)\\.(\\d\\d|\\d)-(\\d\\d|\\d)\\.(\\d\\d|\\d)", value: surfaceForm)
    }
    
    /// Checks if a given surface form matches to a date form. It should be something like 3/10/2023 or 2.3.2012
    /// - Parameter surfaceForm: Surface form to be checked.
    /// - Returns: True if the surface form is in date form
    private func isDate(surfaceForm: String) -> Bool{
        return patternMatches(expr: "(\\d\\d|\\d)/(\\d\\d|\\d)/\\d+", value: surfaceForm) || patternMatches(expr: "(\\d\\d|\\d)\\.(\\d\\d|\\d)\\.\\d+", value: surfaceForm)
    }
    
    /**
     * The morphologicalAnalysis method is used to analyse a FsmParseList by comparing with the regex.
     * It creates an {@link ArrayList} fsmParse to hold the result of the analysis method. For each surfaceForm input,
     * it gets a substring and considers it as a possibleRoot. Then compares with the regex.
     * <p>
     * If the surfaceForm input string matches with Turkish chars like Ç, Ş, İ, Ü, Ö, it adds the surfaceForm to Trie with IS_OA tag.
     * If the possibleRoot contains /, then it is added to the Trie with IS_KESIR tag.
     * If the possibleRoot contains \d\d|\d)/(\d\d|\d)/\d+, then it is added to the Trie with IS_DATE tag.
     * If the possibleRoot contains \\d\d|\d, then it is added to the Trie with IS_PERCENT tag.
     * If the possibleRoot contains \d\d|\d):(\d\d|\d):(\d\d|\d), then it is added to the Trie with IS_ZAMAN tag.
     * If the possibleRoot contains \d+-\d+, then it is added to the Trie with IS_RANGE tag.
     * If the possibleRoot is an Integer, then it is added to the Trie with IS_SAYI tag.
     * If the possibleRoot is a Double, then it is added to the Trie with IS_REELSAYI tag.
        - Parameters:
            - surfaceForm: String to analyse.
        - Returns: fsmParseList which holds the analysis.
     */
    public func morphologicalAnalysis(surfaceForm: String) -> FsmParseList{
        var fsmParseList : FsmParseList
        if parsedSurfaceForms != nil && !parsedSurfaceForms!.contains(Word.lowercase(s: surfaceForm)) && !isInteger(surfaceForm: surfaceForm) && !isDouble(surfaceForm: surfaceForm) && !isPercent(surfaceForm: surfaceForm) && !isTime(surfaceForm: surfaceForm) && !isRange(surfaceForm: surfaceForm) && !isDate(surfaceForm: surfaceForm) {
            return FsmParseList(fsmParses: [])
        }
        if cache != nil && cache!.contains(key: surfaceForm) {
            return cache!.get(key: surfaceForm)!
        }
        if patternMatches(expr: "(\\w|Ç|Ş|İ|Ü|Ö)\\.", value: surfaceForm) {
            dictionaryTrie.addWord(word: Word.lowercase(s: surfaceForm), root: TxtWord(name: Word.lowercase(s: surfaceForm), flag: "IS_OA"))
        }
        let defaultFsmParse : [FsmParse] = analysis(surfaceForm: Word.lowercase(s: surfaceForm), isProper: isProperNoun(surfaceForm: surfaceForm))
        if defaultFsmParse.count > 0 {
            fsmParseList = FsmParseList(fsmParses: defaultFsmParse)
            if cache != nil {
                cache!.add(key: surfaceForm, data: fsmParseList)
            }
            return fsmParseList
        }
        var fsmParse : [FsmParse] = []
        if surfaceForm.contains("'") {
            let possibleRoot : String = String(surfaceForm[..<surfaceForm.range(of: "'")!.lowerBound])
            if possibleRoot != "" {
                if possibleRoot.contains("/") || possibleRoot.contains("\\/") {
                    dictionaryTrie.addWord(word: possibleRoot, root: TxtWord(name: possibleRoot, flag: "IS_KESIR"))
                    fsmParse = analysis(surfaceForm: Word.lowercase(s: surfaceForm), isProper: isProperNoun(surfaceForm: surfaceForm))
                } else {
                    if isDate(surfaceForm: possibleRoot) {
                        dictionaryTrie.addWord(word: possibleRoot, root: TxtWord(name: possibleRoot, flag: "IS_DATE"))
                        fsmParse = analysis(surfaceForm: Word.lowercase(s: surfaceForm), isProper: isProperNoun(surfaceForm: surfaceForm))
                    } else {
                        if patternMatches(expr: "\\d+/\\d+", value: possibleRoot) {
                            dictionaryTrie.addWord(word: possibleRoot, root: TxtWord(name: possibleRoot, flag: "IS_KESIR"))
                            fsmParse = analysis(surfaceForm: Word.lowercase(s: surfaceForm), isProper: isProperNoun(surfaceForm: surfaceForm))
                        } else {
                            if isPercent(surfaceForm: possibleRoot) {
                                dictionaryTrie.addWord(word: possibleRoot, root: TxtWord(name: possibleRoot, flag: "IS_PERCENT"))
                                fsmParse = analysis(surfaceForm: Word.lowercase(s: surfaceForm), isProper: isProperNoun(surfaceForm: surfaceForm))
                            } else {
                                if isTime(surfaceForm: surfaceForm) {
                                    dictionaryTrie.addWord(word: possibleRoot, root: TxtWord(name: possibleRoot, flag: "IS_ZAMAN"))
                                    fsmParse = analysis(surfaceForm: Word.lowercase(s: surfaceForm), isProper: isProperNoun(surfaceForm: surfaceForm))
                                } else {
                                    if isRange(surfaceForm: surfaceForm) {
                                        dictionaryTrie.addWord(word: possibleRoot, root: TxtWord(name: possibleRoot, flag: "IS_RANGE"))
                                        fsmParse = analysis(surfaceForm: Word.lowercase(s: surfaceForm), isProper: isProperNoun(surfaceForm: surfaceForm))
                                    } else {
                                        if isInteger(surfaceForm: possibleRoot) {
                                            dictionaryTrie.addWord(word: possibleRoot, root: TxtWord(name: possibleRoot, flag: "IS_SAYI"))
                                            fsmParse = analysis(surfaceForm: Word.lowercase(s: surfaceForm), isProper: isProperNoun(surfaceForm: surfaceForm))
                                        } else {
                                            if (isDouble(surfaceForm: possibleRoot)) {
                                                dictionaryTrie.addWord(word: possibleRoot, root: TxtWord(name: possibleRoot, flag: "IS_REELSAYI"))
                                                fsmParse = analysis(surfaceForm: Word.lowercase(s: surfaceForm), isProper: isProperNoun(surfaceForm: surfaceForm))
                                            } else {
                                                if (Word.isCapital(surfaceForm: possibleRoot)) {
                                                    var newWord : TxtWord? = nil
                                                    if (dictionary.getWord(name: Word.lowercase(s: possibleRoot)) != nil) {
                                                        (dictionary.getWord(name: Word.lowercase(s: possibleRoot)) as! TxtWord).addFlag(flag: "IS_OA")
                                                    } else {
                                                        newWord = TxtWord(name: Word.lowercase(s: possibleRoot), flag: "IS_OA")
                                                        dictionaryTrie.addWord(word: Word.lowercase(s: possibleRoot), root: newWord!)
                                                    }
                                                    fsmParse = analysis(surfaceForm: Word.lowercase(s: surfaceForm), isProper: isProperNoun(surfaceForm: surfaceForm))
                                                    if fsmParse.count == 0 && newWord != nil {
                                                        newWord!.addFlag(flag: "IS_KIS")
                                                        fsmParse = analysis(surfaceForm: Word.lowercase(s: surfaceForm), isProper: isProperNoun(surfaceForm: surfaceForm))
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
        fsmParseList = FsmParseList(fsmParses: fsmParse)
        if cache != nil && fsmParseList.size() > 0 {
            cache!.add(key: surfaceForm, data: fsmParseList)
        }
        return fsmParseList
    }
    
    /**
     * The morphologicalAnalysisExists method calls analysisExists to check the existence of the analysis with given
     * root and surfaceForm.
        - Parameters:
            - surfaceForm: String to check.
            - rootWord :   TxtWord input root.
        - Returns: true an analysis exists, otherwise return false.
     */
    public func morphologicalAnalysisExists(rootWord: TxtWord, surfaceForm: String) -> Bool {
        return analysisExists(rootWord: rootWord, surfaceForm: Word.lowercase(s: surfaceForm), isProper: true)
    }

}

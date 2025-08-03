//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 10.03.2021.
//

import Foundation


public class Transition{
    
    private var _toState : FsmState?
    private var _with : String?
    private var _withName : String?
    private var _toPos : String?
    
    /**
     * A constructor of {@link Transition} class which takes  a {@link State}, and two {@link String}s as input. Then it
     * initializes toState, with and withName variables with given inputs.
        - Parameters:
            - toState:  {@link State} input.
            - with :    String input.
            - withName: String input.
     */
    public init(toState: FsmState?, with: String, withName: String?){
        self._toState = toState
        self._with = with
        self._withName = withName
        _toPos = nil
    }
    
    /**
     * Another constructor of {@link Transition} class which takes  a {@link State}, and three {@link String}s as input. Then it
     * initializes toState, with, withName and toPos variables with given inputs.
        - Parameters:
            - toState:  {@link State} input.
            - with:     String input.
            - withName: String input.
            - toPos:    String input.
     */
    public init(toState: FsmState, with: String, withName: String?, toPos: String){
        self._toState = toState
        self._with = with
        self._withName = withName
        self._toPos = toPos
    }
    
    /**
     * Another constructor of {@link Transition} class which only takes a {@link String}s as an input. Then it
     * initializes toState, withName and toPos variables as null and with variable with the given input.
        - Parameters:
            - with: String input.
     */
    public init(with: String){
        _toState = nil
        _withName = nil
        _toPos = nil
        self._with = with
    }
    
    /**
     * Getter for the toState variable.
        - Returns: toState variable.
     */
    public func getToState() -> FsmState?{
        return _toState
    }
    
    /**
     * Getter for the toPos variable.
        - Returns: toPos variable.
     */
    public func toPos() -> String?{
        return _toPos
    }
    
    /**
     * The transitionPossible method takes two {@link String} as inputs; currentSurfaceForm and realSurfaceForm. If the
     * length of the given currentSurfaceForm is greater than the given realSurfaceForm, it directly returns true. If not,
     * it takes a substring from given realSurfaceForm with the size of currentSurfaceForm. Then checks for the characters of
     * with variable.
     * <p>
     * If the character of with that makes transition is C, it returns true if the substring contains c or ç.
     * If the character of with that makes transition is D, it returns true if the substring contains d or t.
     * If the character of with that makes transition is A, it returns true if the substring contains a or e.
     * If the character of with that makes transition is K, it returns true if the substring contains k, g or ğ.
     * If the character of with that makes transition is other than the ones above, it returns true if the substring
     * contains the same character as with.
        - Parameters:
            - currentSurfaceForm: {@link String} input.
            - realSurfaceForm:    {@link String} input.
        - Returns: True when the transition is possible according to Turkish grammar, false otherwise.
     */
    public func transitionPossible(currentSurfaceForm: String, realSurfaceForm: String) -> Bool{
        if currentSurfaceForm.count == 0 || currentSurfaceForm.count >= realSurfaceForm.count {
            return true
        }
        let searchString : String = String(realSurfaceForm.suffix(realSurfaceForm.count - currentSurfaceForm.count))
        for i in 0..<_with!.count {
            switch Word.charAt(s: _with!, i: i) {
                case "C":
                    return searchString.contains("c") || searchString.contains("ç")
                case "D":
                    return searchString.contains("d") || searchString.contains("t")
                case "c", "e", "r", "p", "l", "b", "g", "o", "m", "v", "i", "ü", "z":
                    return searchString.contains(Word.charAt(s: _with!, i: i))
                case "A":
                    return searchString.contains("a") || searchString.contains("e")
                case "k":
                    return searchString.contains("k") || searchString.contains("g") || searchString.contains("ğ")
                default:
                    break;
            }
        }
        return true;
    }
    
    /**
     * The transitionPossible method takes a {@link FsmParse} currentFsmParse as an input. It then checks some special cases;
        - Parameters:
            - currentFsmParse: Parse to be checked
        - Returns: True if transition is possible false otherwise
     */
    public func transitionPossible(currentFsmParse: FsmParse) -> Bool{
        if _with == "Ar" && currentFsmParse.getSurfaceForm().hasSuffix("l") && currentFsmParse.getWord().getName() != currentFsmParse.getSurfaceForm() {
            return false
        }
        if currentFsmParse.getVerbAgreement() != nil && currentFsmParse.getPossessiveAgreement() != nil && _withName != nil {
            if currentFsmParse.getVerbAgreement() == "A3PL" && _withName == "^DB+VERB+ZERO+PRES+A1SG" {
                return false
            }
            if currentFsmParse.getVerbAgreement() == "A3SG" && (currentFsmParse.getPossessiveAgreement() == "P1SG" || currentFsmParse.getPossessiveAgreement() == "P2SG") && _withName == "^DB+VERB+ZERO+PRES+A1PL" {
                return false
            }
        }
        return true
    }
    
    /// The transitionPossible method takes root and current parse as inputs. It then checks some special cases.
    /// - Parameters:
    ///   - root: Current root word
    ///   - fromState: From which state we arrived to this state.
    /// - Returns: true if transition is possible false otherwise
        public func transitionPossible(root: TxtWord, fromState: FsmState) -> Bool{
        if root.isAdjective() && ((root.isNominal() && !root.isExceptional()) || root.isPronoun()) && _toState!.getName() == "NominalRoot(ADJ)" && _with == "0" {
            return false
        }
        if root.isAdjective() && root.isNominal() && _with == "^DB+VERB+ZERO+PRES+A3PL" && fromState.getName() == "AdjectiveRoot" {
            return false;
        }
        if root.isAdjective() && root.isNominal() && _with == "SH" && fromState.getName() == "AdjectiveRoot" {
            return false
        }
        if _with == "ki" {
            return root.takesRelativeSuffixKi()
        }
        if _with == "kü" {
            return root.takesRelativeSuffixKu()
        }
        if _with == "DHr" {
            if _toState!.getName() == "Adverb" {
                return true
            } else {
                return root.takesSuffixDIRAsFactitive()
            }
        }
        if _with == "Hr" && (_toState!.getName() == "AdjectiveRoot(VERB)" || _toState!.getName() == "OtherTense" || _toState!.getName() == "OtherTense2") {
            return root.takesSuffixIRAsAorist()
        }
        return true
    }
    
    /**
     * The withFirstChar method returns the first character of the with variable.
     *
        - Returns: The first character of the with variable.
     */
    private func withFirstChar() -> Character{
        if _with?.count == 0 {
            return "$"
        }
        if Word.charAt(s: _with!, i: 0) != "'" {
            return Word.charAt(s: _with!, i: 0)
        } else {
            if _with?.count == 1 {
                return Word.charAt(s: _with!, i: 0)
            } else {
                return Word.charAt(s: _with!, i: 1)
            }
        }
    }
    
    /**
     * The startWithVowelorConsonantDrops method checks for some cases. If the first character of with variable is "nsy",
     * and with variable does not equal to one of the Strings; "ylA, ysA, ymHs, yDH, yken", it returns true. If
     * <p>
     * Or, if the first character of with variable is 'A, H: or any other vowels, it returns true.
     *
        - Returns: True if it starts with vowel or consonant drops, false otherwise.
     */
    private func startWithVowelorConsonantDrops() -> Bool{
        if TurkishLanguage.isConsonantDrop(ch: withFirstChar()) && _with != "ylA" && _with != "ysA" && _with != "ymHs" && _with != "yDH" && _with != "yken" {
            return true
        }
        if withFirstChar() == "A" || withFirstChar() == "H" || TurkishLanguage.isVowel(ch: withFirstChar()) {
            return true
        }
        return false
    }
    
    /**
     * The softenDuringSuffixation method takes a {@link TxtWord} root as an input. It checks two cases; first case returns
     * true if the given root is nominal or adjective and has one of the flags "IS_SD, IS_B_SD, IS_SDD" and with variable
     * equals o one of the Strings "Hm, nDAn, ncA, nDA, yA, yHm, yHz, yH, nH, nA, nHn, H, sH, Hn, HnHz, HmHz".
     * <p>
     * And the second case returns true if the given root is verb and has the "F_SD" flag, also with variable starts with
     * "Hyor" or equals one of the Strings "yHs, yAn, yA, yAcAk, yAsH, yHncA, yHp, yAlH, yArAk, yAdur, yHver, yAgel, yAgor,
     * yAbil, yAyaz, yAkal, yAkoy, yAmA, yHcH, HCH, Hr, Hs, Hn, yHn", yHnHz, Ar, Hl").
        - Parameters:
            - root {@link TxtWord} input.
        - Returns: true if there is softening during suffixation of the given root, false otherwise.
     */
    public func softenDuringSuffixation(root: TxtWord) -> Bool{
        if (root.isNominal() || root.isAdjective()) && root.nounSoftenDuringSuffixation() && (_with == "Hm" || _with == "nDAn" || _with == "ncA" || _with == "nDA" || _with == "yA" || _with == "yHm" || _with == "yHz" || _with == "yH" || _with == "nH" || _with == "nA" || _with == "nHn" || _with == "H" || _with == "sH" || _with == "Hn" || _with == "HnHz" || _with == "HmHz") {
            return true
        }
        if root.isVerb() && root.verbSoftenDuringSuffixation() && (_with!.hasPrefix("Hyor") || _with == "yHs" || _with == "yAn" || _with == "yA" || _with!.hasPrefix("yAcAk") || _with == "yAsH" || _with == "yHncA" || _with == "yHp" || _with == "yAlH" || _with == "yArAk" || _with == "yAdur" || _with == "yHver" || _with == "yAgel" || _with == "yAgor" || _with == "yAbil" || _with == "yAyaz" || _with == "yAkal" || _with == "yAkoy" || _with == "yAmA" || _with == "yHcH" || _with == "HCH" || _with!.hasPrefix("Hr") || _with == "Hs" || _with == "Hn" || _with == "yHn" || _with == "yHnHz" || _with!.hasPrefix("Ar") || _with == "Hl") {
            return true
        }
        return false
    }
    
    /**
     * The makeTransition method takes a {@link TxtWord} root and s {@link String} stem as inputs. If given root is a verb,
     * it makes transition with given root and stem with the verbal root state. If given root is not verb, it makes transition
     * with given root and stem and the nominal root state.
        - Parameters:
            - root: {@link TxtWord} input.
            - stem: String input.
        - Returns: String type output that has the transition.
     */
    public func makeTransition(root: TxtWord, stem: String) -> String{
        if (root.isVerb()) {
                        return makeTransition(root: root, stem: stem, startState: FsmState(name: "VerbalRoot", startState: true, endState: false))
        } else {
                        return makeTransition(root: root, stem: stem, startState: FsmState(name: "NominalRoot", startState: true, endState: false))
        }
    }
    
    /// The method is main driving method to accomplish the current transition from one state to another depending on
    /// the root form of the word, current value of the word form, and the type of the start state. The method
    /// (a) returns the original word form if the transition is an epsilon transition, (b) adds 'nunla' if the current
    /// stem is 'bu', 'şu' or 'o', (c) returns 'bana' or 'sana' if the current stem is 'ben' or 'sen' respectively.
    /// For other cases, the method first modifies current stem and then adds the transition using special metamorpheme
    /// resolving methods. These cases are: (d) Converts 'y' of the first character of the transition to 'i' if the
    /// current stem is 'ye' or 'de'. (e) Drops the last two characters and adds last character when the transition is
    /// ('Hl' or 'Hn') and last 'I' drops during passive suffixation. (f) Adds 'y' character when the word ends with 'su'
    /// and the transition does not start with 'y'. (g) Adds the last character again when the root duplicates during
    /// suffixation. (h) Drops the last two characters and adds the last character when last 'i' drops during
    /// suffixation. (i) Replaces the last character with a soft one when the root soften during suffixation.
    /// - Parameters:
    ///   - root: Root of the current word form
    ///   - stem: Current word form
    ///   - startState: The state from which this Fsm morphological analysis search has started.
    /// - Returns: The current value of the word form after this transition is completed in the finite state machine.
        public func makeTransition(root: TxtWord, stem: String, startState: FsmState) -> String{
        let rootWord : Bool = root.getName() == stem || (root.getName() + "'") == stem
        var formation : String = stem
        var i : Int = 0
        if _with == "0" {
            return stem
        }
        if (stem == "bu" || stem == "şu" || stem == "o") && rootWord && _with == "ylA" {
            return stem + "nunla"
        }
        if _with == "yA" {
            if stem == "ben" {
                return "bana"
            }
            if stem == "sen" {
                return "sana"
            }
        }
        var formationToCheck : String = stem
        //---vowelEChangesToIDuringYSuffixation---
        //de->d(i)yor, ye->y(i)yor
        if rootWord && withFirstChar() == "y" && root.vowelEChangesToIDuringYSuffixation() && (Word.charAt(s: _with!, i: 1) != "H" || root.getName() == "ye") {
            formation = stem.prefix(stem.count - 1) + "i"
            formationToCheck = formation
        } else {
            //---lastIdropsDuringPassiveSuffixation---
            // yoğur->yoğrul, ayır->ayrıl, buyur->buyrul, çağır->çağrıl, çevir->çevril, devir->devril,
            // kavur->kavrul, kayır->kayrıl, kıvır->kıvrıl, savur->savrul, sıyır->sıyrıl, yoğur->yoğrul
            if rootWord && (_with == "Hl" || _with == "Hn") && root.lastIdropsDuringPassiveSuffixation() {
                formation = stem.prefix(stem.count - 2) + String(Word.charAt(s: stem, i: stem.count - 1))
                formationToCheck = stem
            } else {
                //---showsSuRegularities---
                //karasu->karasuyu, su->suyu, ağırsu->ağırsuyu, akarsu->akarsuyu, bengisu->bengisuyu
                if rootWord && root.showsSuRegularities() && startWithVowelorConsonantDrops() && !_with!.hasPrefix("y") {
                    formation = stem + "y"
                    formationToCheck = formation
                } else {
                    if rootWord && root.duplicatesDuringSuffixation() && !startState.getName().hasPrefix("VerbalRoot") && TurkishLanguage.isConsonantDrop(ch: Word.charAt(s: _with!, i: 0)) {
                        //---duplicatesDuringSuffixation---
                        if softenDuringSuffixation(root: root) {
                            //--extra softenDuringSuffixation
                            switch (Word.lastPhoneme(stem: stem)) {
                                case "p":
                                    //tıp->tıbbı
                                    formation = stem.prefix(stem.count - 1) + "bb"
                                    break;
                                case "t":
                                    //cet->ceddi, met->meddi, ret->reddi, serhat->serhaddi, zıt->zıddı, şet->şeddi
                                    formation = stem.prefix(stem.count - 1) + "dd"
                                    break;
                                default:
                                    break;
                            }
                        } else {
                            //cer->cerri, emrihak->emrihakkı, fek->fekki, fen->fenni, had->haddi, hat->hattı,
                            // haz->hazzı, his->hissi
                            formation = stem + String(Word.charAt(s: stem, i: stem.count - 1))
                        }
                        formationToCheck = formation
                    } else {
                        if rootWord && root.lastIdropsDuringSuffixation() && !startState.getName().hasPrefix("VerbalRoot") && !startState.getName().hasPrefix("ProperRoot") && startWithVowelorConsonantDrops() {
                            //---lastIdropsDuringSuffixation---
                            if softenDuringSuffixation(root: root) {
                                //---softenDuringSuffixation---
                                switch (Word.lastPhoneme(stem: stem)) {
                                    case "p":
                                        //hizip->hizbi, kayıp->kaybı, kayıt->kaydı, kutup->kutbu
                                        formation = stem.prefix(stem.count - 2) + "b"
                                        break
                                    case "t":
                                        //akit->akdi, ahit->ahdi, lahit->lahdi, nakit->nakdi, vecit->vecdi
                                        formation = stem.prefix(stem.count - 2) + "d"
                                        break
                                    case "ç":
                                        //eviç->evci, nesiç->nesci
                                        formation = stem.prefix(stem.count - 2) + "c"
                                        break
                                    default:
                                        break
                                }
                            } else {
                                //sarıağız->sarıağzı, zehir->zehri, zikir->zikri, nutuk->nutku, omuz->omzu, ömür->ömrü
                                //lütuf->lütfu, metin->metni, kavim->kavmi, kasıt->kastı
                                formation = stem.prefix(stem.count - 2) + String(Word.charAt(s: stem, i: (stem.count - 1)))
                            }
                            formationToCheck = stem
                        } else {
                            switch (Word.lastPhoneme(stem: stem)) {
                                //---nounSoftenDuringSuffixation or verbSoftenDuringSuffixation
                                case "p":
                                    //adap->adabı, amip->amibi, azap->azabı, gazap->gazabı
                                    if startWithVowelorConsonantDrops() && rootWord && softenDuringSuffixation(root: root) {
                                        formation = stem.prefix(stem.count - 1) + "b"
                                    }
                                    break;
                                case "t":
                                    //adet->adedi, akort->akordu, armut->armudu
                                    //affet->affedi, yoket->yokedi, sabret->sabredi, rakset->raksedi
                                    if startWithVowelorConsonantDrops() && rootWord && softenDuringSuffixation(root: root) {
                                        formation = stem.prefix(stem.count - 1) + "d"
                                    }
                                    break;
                                case "ç":
                                    //ağaç->ağacı, almaç->almacı, akaç->akacı, avuç->avucu
                                    if startWithVowelorConsonantDrops() && rootWord && softenDuringSuffixation(root: root) {
                                        formation = stem.prefix(stem.count - 1) + "c"
                                    }
                                    break;
                                case "g":
                                    //arkeolog->arkeoloğu, filolog->filoloğu, minerolog->mineroloğu
                                    if startWithVowelorConsonantDrops() && rootWord && softenDuringSuffixation(root: root) {
                                        formation = stem.prefix(stem.count - 1) + "ğ"
                                    }
                                    break;
                                case "k":
                                    //ahenk->ahengi, künk->küngü, renk->rengi, pelesenk->pelesengi
                                    if startWithVowelorConsonantDrops() && rootWord && root.endingKChangesIntoG() && (!root.isProperNoun() || startState.description() != "ProperRoot") {
                                        formation = stem.prefix(stem.count - 1) + "g"
                                    } else {
                                        //ablak->ablağı, küllük->küllüğü, kitaplık->kitaplığı, evcilik->evciliği
                                        if startWithVowelorConsonantDrops() && (!rootWord || (softenDuringSuffixation(root: root) && (!root.isProperNoun() || startState.description() != "ProperRoot"))) {
                                            formation = stem.prefix(stem.count - 1) + "ğ"
                                        }
                                    }
                                    break;
                                default:
                                    break;
                            }
                            formationToCheck = formation
                        }
                    }
                }
            }
        }
        if TurkishLanguage.isConsonantDrop(ch: withFirstChar()) && !TurkishLanguage.isVowel(ch: Word.charAt(s: stem, i: stem.count - 1)) && (root.isNumeral() || root.isReal() || root.isFraction() || root.isTime() || root.isDate() || root.isPercent() || root.isRange()) && (root.getName().hasSuffix("1") || root.getName().hasSuffix("3") || root.getName().hasSuffix("4") || root.getName().hasSuffix("5") || root.getName().hasSuffix("8") || root.getName().hasSuffix("9") || root.getName().hasSuffix("10") || root.getName().hasSuffix("30") || root.getName().hasSuffix("40") || root.getName().hasSuffix("60") || root.getName().hasSuffix("70") || root.getName().hasSuffix("80") || root.getName().hasSuffix("90") || root.getName().hasSuffix("00")) {
            if Word.charAt(s: _with!, i: 0) == "'" {
                formation = formation + "'"
                i = 2
            } else {
                i = 1
            }
        } else {
            if ((TurkishLanguage.isConsonantDrop(ch: withFirstChar()) && TurkishLanguage.isConsonant(ch: Word.lastPhoneme(stem: stem))) || (rootWord && root.consonantSMayInsertedDuringPossesiveSuffixation())) {
                if Word.charAt(s: _with!, i: 0) == "'" {
                    formation = formation + "'"
                    if root.isAbbreviation(){
                        i = 1;
                    } else {
                        i = 2
                    }
                } else {
                    i = 1
                }
            }
        }
        while i < _with!.count {
            switch Word.charAt(s: _with!, i: i) {
                case "D":
                    formation = MorphotacticEngine.resolveD(root: root, formation: formation, formationToCheck: formationToCheck)
                    break;
                case "A":
                    formation = MorphotacticEngine.resolveA(root: root, formation: formation, rootWord: rootWord, formationToCheck: formationToCheck)
                    break;
                case "H":
                    if Word.charAt(s: _with!, i: 0) != "'" {
                        formation = MorphotacticEngine.resolveH(root: root, formation: formation, beginningOfSuffix: i == 0, specialCaseTenseSuffix: (_with?.hasPrefix("Hyor"))!, rootWord: rootWord, formationToCheck: formationToCheck)
                    } else {
                        formation = MorphotacticEngine.resolveH(root: root, formation: formation, beginningOfSuffix: i == 1, specialCaseTenseSuffix: false, rootWord: rootWord, formationToCheck: formationToCheck)
                    }
                    break;
                case "C":
                    formation = MorphotacticEngine.resolveC(formation: formation, formationToCheck: formationToCheck)
                    break;
                case "S":
                    formation = MorphotacticEngine.resolveS(formation: formation)
                    break;
                case "Ş":
                    formation = MorphotacticEngine.resolveSh(formation: formation)
                    break;
                default:
                    if (i == _with!.count - 1 && Word.charAt(s: _with!, i: i) == "s") {
                        formation += "ş"
                    } else {
                        formation += String(Word.charAt(s: _with!, i: i))
                    }
            }
            formationToCheck = formation
            i += 1
        }
        return formation
    }
        
    public func description() -> String{
        return _with!
    }
    
    /**
     * The with method returns the withName variable.
     *
        - Returns: the withName variable.
     */
    public func with() -> String?{
        return _withName
    }
}

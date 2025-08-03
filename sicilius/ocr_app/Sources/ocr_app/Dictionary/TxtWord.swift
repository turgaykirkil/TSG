//
//  TxtWord.swift
//  
//
//  Created by Olcay Taner YILDIZ on 6.09.2020.
//

import Foundation

public class TxtWord : Word, NSCopying{
    
    private var __flags: [String] = []
    private var __morphology: String = ""

    /**
     A constructor of TxtWord class which takes a String name as an input and calls its super class Word
    with given name. Then, creates a new array as flags.

    - Parameters:
        - name : Name of the word.
    */
    public override init(name: String){
        super.init(name: name)
    }
    
    /// Another constructor of TxtWord class which takes a String name and a flag as inputs and calls its super class Word
    /// with given name. Then, creates a new {@link ArrayList} as flags and calls addFlag method with given flag.
    /// - Parameters:
    ///   - name: Name of the word
    ///   - flag: Initial flag of the word
    public init(name: String, flag: String){
        super.init(name: name)
        self.__flags.append(flag)
    }
    
    /// Clone method for the TxtWord class. Creates a copy of current word.
    /// - Parameter zone: -
    /// - Returns: Copy of the TxtWord
    public func copy(with zone: NSZone? = nil) -> Any {
        let copy : TxtWord = TxtWord(name: self.getName())
        copy.__flags = []
        for flag in self.__flags{
            copy.__flags.append(flag)
        }
        return copy
    }
    
    /**
    The addFlag method takes a String flag as an input and adds given flag to the flags list.

    - Parameter flag : String input to add.
    */
    public func addFlag(flag: String){
        self.__flags.append(flag)
    }

    /**
    The removeFlag method takes a String flag as an input and removes given flag from the flags list.

    - Parameter flag : String input to remove.
    */
    public func removeFlag(flag: String){
        self.__flags.remove(at: self.__flags.firstIndex(of: flag)!)
    }
    
    /// Accessor for the inner morphology of the word.
    /// - Returns: Inner morphology of the word.
    public func getMorphology()->String{
        return self.__morphology
    }
    
    /// Mutator for the inner morphology of the word.
    /// - Parameter morphology: New inner morphology of the word.
    public func setMorphology(morphology: String){
        self.__morphology = morphology
    }

    /**
    The verbType method checks flags list and returns the corresponding cases.

    - Returns: the corresponding cases.
    */
    public func verbType() -> String{
        if self.__flags.contains("F1P1-NO-REF"){
            return "F1P1-NO-REF"
        }
        if self.__flags.contains("F2P1-NO-REF"){
            return "F2P1-NO-REF"
        }
        if self.__flags.contains("F3P1-NO-REF"){
            return "F3P1-NO-REF"
        }
        if self.__flags.contains("F4P1-NO-REF"){
            return "F4P1-NO-REF"
        }
        if self.__flags.contains("F4PR-NO-REF"){
            return "F4PR-NO-REF"
        }
        if self.__flags.contains("F4PL-NO-REF"){
            return "F4PL-NO-REF"
        }
        if self.__flags.contains("F4PW-NO-REF"){
            return "F4PW-NO-REF"
        }
        if self.__flags.contains("F5PL-NO-REF"){
            return "F5PL-NO-REF"
        }
        if self.__flags.contains("F5PR-NO-REF"){
            return "F5PR-NO-REF"
        }
        if self.__flags.contains("F5PW-NO-REF"){
            return "F5PW-NO-REF"
        }
        if self.__flags.contains("F1P1"){
            return "F1P1"
        }
        if self.__flags.contains("F2P1"){
            return "F2P1"
        }
        if self.__flags.contains("F2PL"){
            return "F2PL"
        }
        if self.__flags.contains("F3P1"){
            return "F3P1"
        }
        if self.__flags.contains("F4P1"){
            return "F4P1"
        }
        if self.__flags.contains("F4PR"){
            return "F4PR"
        }
        if self.__flags.contains("F4PL"){
            return "F4PL"
        }
        if self.__flags.contains("F4PW"){
            return "F4PW"
        }
        if self.__flags.contains("F5P1"){
            return "F5P1"
        }
        if self.__flags.contains("F5PL"){
            return "F5PL"
        }
        if self.__flags.contains("F5PR"){
            return "F5PR"
        }
        if self.__flags.contains("F5PW"){
            return "F5PW"
        }
        if self.__flags.contains("F6P1"){
            return "F6P1"
        }
        return ""
    }

    /**
    The samePos method takes TxtWord as input and returns true if;

    flags list contains CL_ISIM
    CL_ISIM: The bare-form of the word is a noun. e.g. Abla

    flags list contains CL_FIIL
    CL_FIIL: The bare-form of the word is a verb. e.g. Affet

    flags list contains IS_ADJ
    IS_ADJ: The bare-form of the word is a adjective. e.g. Acayip

    flags list contains IS_ZM
    IS_ZM: The bare-form of the word is a pronoun. e.g. Başkası

    flags list contains IS_ADVERB
    IS_ADVERB: The bare-form of the word is a adverb. e.g. Tekrar, açıktan, adeta

    - Parameter word : TxtWord type input.

    - Returns: true if given word is nominal, verb, adjective, pronoun or adverb, false otherwise.
    */
    public func samePos(word: TxtWord) -> Bool{
        if self.isNominal() && word.isNominal(){
            return true
        }
        if self.isVerb() && word.isVerb(){
            return true
        }
        if self.isAdjective() && word.isAdjective(){
            return true
        }
        if self.isPronoun() && word.isPronoun(){
            return true
        }
        if self.isAdverb() && word.isAdverb(){
            return true
        }
        return false
    }

    /**
    The isNominal method returns true if flags list contains CL_ISIM.

    - Returns: true if flags list contains CL_ISIM.
    */
    public func isNominal() -> Bool{
        return self.__flags.contains("CL_ISIM")
    }

    /**
    The isPassive method returns true if flags list contains PASSIVE-HN.

    - Returns: true if flags list contains PASSIVE-HN.
    */
    public func isPassive() -> Bool{
        return self.__flags.contains("PASSIVE-HN")
    }

    /**
    The isAbbreviation method returns true if flags list contains IS_KIS.

    - Returns: true if flags list contains IS_KIS.
    */
    public func isAbbreviation() -> Bool{
        return self.__flags.contains("IS_KIS")
    }

    /**
    The isInterjection method returns true if flags list contains IS_INTERJ.

    - Returns: true if flags list contains IS_INTERJ.
    */
    public func isInterjection() -> Bool{
        return self.__flags.contains("IS_INTERJ")
    }

    /**
    The isDuplicate method returns true if flags list contains IS_DUP.

    - Returns: true if flags list contains IS_DUP.
    */
    public func isDuplicate() -> Bool{
        return self.__flags.contains("IS_DUP")
    }

    /**
     The isDuplicate method returns true if flags list contains IS_CODE.
     
     - Returns: true if flags list contains IS_CODE.
     */
    public func isCode() -> Bool{
        return self.__flags.contains("IS_CODE")
    }

    /**
     The isDuplicate method returns true if flags list contains IS_METRIC.
     
     - Returns: true if flags list contains IS_METRIC.
     */
    public func isMetric() -> Bool{
        return self.__flags.contains("IS_METRIC")
    }

    /**
    The isHeader method returns true if flags list contains IS_HEADER.

    - Returns: true if flags list contains IS_HEADER.
    */
    public func isHeader() -> Bool{
        return self.__flags.contains("IS_HEADER")
    }

    /**
    The isAdjective method returns true if flags list contains IS_ADJ.

    - Returns: true if flags list contains IS_ADJ.
    */
    public func isAdjective() -> Bool{
        return self.__flags.contains("IS_ADJ")
    }

    /**
    The isPureAdjective method returns true if flags list contains IS_PUREADJ.

    - Returns: true if flags list contains IS_PUREADJ.
    */
    public func isPureAdjective() -> Bool{
        return self.__flags.contains("IS_PUREADJ")
    }

    /**
    The isPronoun method returns true if flags list contains IS_ZM.
    IS_ZM: The bare-form of the word is a pronoun. e.g. Hangi, hep, hiçbiri

    - Returns: true if flags list contains IS_ZM.
    */
    public func isPronoun() -> Bool{
        return self.__flags.contains("IS_ZM")
    }

    /**
    The isQuestion method returns true if flags list contains IS_QUES.
    IS_QUES: The bare-form of the word is a question. e.g. Mi, mu, mü

    - Returns: true if flags list contains IS_QUES.
    */
    public func isQuestion() -> Bool{
        return self.__flags.contains("IS_QUES")
    }

    /**
    The isVerb method returns true if flags list contains CL_FIIL.

    - Returns: true if flags list contains CL_FIIL.
    */
    public func isVerb() -> Bool{
        return self.__flags.contains("CL_FIIL")
    }

    /**
    The isPortmanteau method returns true if flags list contains IS_BILEŞ.
    IS_BILEŞ: The bare-form is a portmanteau word in affixed form. e.g. gelinçiçeği

    - Returns: true if flags list contains IS_BILEŞ.
    */
    public func isPortmanteau() -> Bool{
        return self.__flags.contains("IS_BILEŞ")
    }

    /**
    The isDeterminer method returns true if flags list contains IS_DET.
    IS_DET: The bare-form of the word is a determiner. e.g. Bazı, bir

    - Returns: true if flags list contains IS_DET.
    */
    public func isDeterminer() -> Bool{
        return self.__flags.contains("IS_DET")
    }

    /**
    The isConjunction method returns true if flags list contains IS_CONJ.
    IS_CONJ: The bare-form of the word is a conjunction. e.g. Gerek, halbuki

    - Returns: true if flags list contains IS_CONJ.
    */
    public func isConjunction() -> Bool{
        return self.__flags.contains("IS_CONJ")
    }

    /**
    The isAdverb method returns true if flags list contains IS_ADVERB.

    - Returns: true if flags list contains IS_ADVERB.
    */
    public func isAdverb() -> Bool{
        return self.__flags.contains("IS_ADVERB")
    }

    /**
    The isPostP method returns true if flags list contains IS_POSTP.
    IS_POSTP: The bare-form of the word is a postposition. e.g. Önce, takdirde, üzere

    - Returns: true if flags list contains IS_POSTP.
    */
    public func isPostP() -> Bool{
        return self.__flags.contains("IS_POSTP")
    }

    /**
    The isPortmanteauEndingWithSI method returns true if flags list contains IS_B_SI.
    IS_B_SI: The bare-form is a portmanteau word ending with "sı". e.g. Giritlalesi

    - Returns: true if flags list contains IS_B_SI.
    */
    public func isPortmanteauEndingWithSI() -> Bool{
        return self.__flags.contains("IS_B_SI")
    }

    /**
    The isPortmanteauFacedVowelEllipsis method returns true if flags list contains IS_B_UD.
    IS_B_UD: The bare-form of the word includes vowel epenthesis,
    therefore the last inserted vowel drops during suffixation. e.g. İnsanoğlu

    - Returns: true if flags list contains IS_B_UD.
    */
    public func isPortmanteauFacedVowelEllipsis() -> Bool{
        return self.__flags.contains("IS_B_UD")
    }

    /**
    The isPortmanteauFacedSoftening method returns true if flags list contains IS_B_SD.
    IS_B_SD: The bare-form of the word includes softening. e.g. Çançiçeği

    - Returns: true if flags list contains IS_B_SD.
    */
    public func isPortmanteauFacedSoftening() -> Bool{
        return self.__flags.contains("IS_B_SD")
    }

    /**
    The isSuffix method returns true if flags list contains EK.
    EK: This tag indicates complementary verbs. e.g. İdi, iken, imiş.

    - Returns: true if flags list contains EK.
    */
    public func isSuffix() -> Bool{
        return self.__flags.contains("EK")
    }

    /**
    The isProperNoun method returns true if flags list contains IS_OA.
    IS_OA: The bare-form of the word is a proper noun. e.g. Abant, Beşiktaş

    - Returns: true if flags list contains IS_OA.
    */
    public func isProperNoun() -> Bool{
        return self.__flags.contains("IS_OA")
    }

    /**
    The isPlural method returns true if flags list contains IS_CA.
    IS_CA: The bare-form of the word is already in a plural form,
    therefore can not take plural suffixes such as "ler" or "lar". e.g. Buğdaygiller

    - Returns: true if flags list contains IS_CA.
    */
    public func isPlural() -> Bool{
        return self.__flags.contains("IS_CA")
    }

    /**
    The isNumeral method returns true if flags list contains IS_SAYI.
    IS_SAYI: The word is a number. e.g. Dört

    - Returns: true if flags list contains IS_SAYI.
    */
    public func isNumeral() -> Bool{
        return self.__flags.contains("IS_SAYI")
    }

    /**
    The isReal method returns true if flags list contains IS_REELSAYI.

    - Returns: true if flags list contains IS_REELSAYI.
    */
    public func isReal() -> Bool{
        return self.__flags.contains("IS_REELSAYI")
    }

    /**
    The isFraction method returns true if flags list contains IS_KESIR.

    - Returns: true if flags list contains IS_KESIR.
    */
    public func isFraction() -> Bool{
        return self.__flags.contains("IS_KESIR")
    }

    /**
    The isTime method returns true if flags list contains IS_ZAMAN.

    - Returns: true if flags list contains IS_ZAMAN.
    */
    public func isTime() -> Bool{
        return self.__flags.contains("IS_ZAMAN")
    }

    /**
    The isDate method returns true if flags list contains IS_DATE.

    - Returns: true if flags list contains IS_DATE.
    */
    public func isDate() -> Bool{
        return self.__flags.contains("IS_DATE")
    }

    /**
    The isPercent method returns true if flags list contains IS_PERCENT.

    - Returns: true if flags list contains IS_PERCENT.
    */
    public func isPercent() -> Bool{
        return self.__flags.contains("IS_PERCENT")
    }

    /**
    The isRange method returns true if flags list contains IS_RANGE.

    - Returns: true if flags list contains IS_RANGE.
    */
    public func isRange() -> Bool{
        return self.__flags.contains("IS_RANGE")
    }

    /**
    The isOrdinal method returns true if flags list contains IS_ORD.
    IS_ORD: The bare-form of the word can take suffixes and these suffixes define a ranking. e.g. Birinci

    - Returns: true if flags list contains IS_ORD.
    */
    public func isOrdinal() -> Bool{
        return self.__flags.contains("IS_ORD")
    }

    /**
    The notObeysVowelHarmonyDuringAgglutination method returns true if flags list contains IS_UU.
    IS_UU: The bare-form does not obey vowel harmony while taking suffixes. e.g. Dikkat

    RETURNS
    -------
    bool
        true if flags list contains IS_UU.
    */
    public func notObeysVowelHarmonyDuringAgglutination() -> Bool{
        return self.__flags.contains("IS_UU")
    }

    /**
    The obeysAndNotObeysVowelHarmonyDuringAgglutination method returns true if flags list contains IS_UUU.
    IS_UUU: The bare-form does not obey vowel harmony while taking suffixes. e.g. Bol, kalp

    - Returns: true if flags list contains IS_UUU.
    */
    public func obeysAndNotObeysVowelHarmonyDuringAgglutination() -> Bool{
        return self.__flags.contains("IS_UUU")
    }

    /**
    The rootSoftenDuringSuffixation method returns true if flags list contains IS_SD, F_SD.

    - Returns: true if flags list contains IS_SD, F_SD.
    */
    public func rootSoftenDuringSuffixation() -> Bool{
        return self.__flags.contains("IS_SD") || self.__flags.contains("F_SD")
    }

    /**
    The rootSoftenAndNotSoftenDuringSuffixation method returns true if flags list contains IS_SDD.
    IS_SDD: The bare-form final consonant can (or can not) get devoiced during vowel-initial suffixation. e.g. Kalp

    - Returns: true if flags list contains IS_SDD.
    */
    public func rootSoftenAndNotSoftenDuringSuffixation() -> Bool{
        return self.__flags.contains("IS_SDD")
    }

    /**
    The verbSoftenDuringSuffixation method returns true if flags list contains F_SD.
    F_SD: The bare-form final consonant gets devoiced during vowel-initial suffixation. e.g. Cezbet

    - Returns: true if flags list contains F_SD.
    */
    public func verbSoftenDuringSuffixation() -> Bool{
        return self.__flags.contains("F_SD")
    }

    /**
    The nounSoftenDuringSuffixation method returns true if flags list contains IS_SD.
    IS_SD: The bare-form final consonant already has an accusative suffix. e.g. Kabağı

    - Returns: true if flags list contains IS_SD.
    */
    public func nounSoftenDuringSuffixation() -> Bool{
        return self.__flags.contains("IS_SD")
    }

    /**
    The endingKChangesIntoG method returns true if flags list contains IS_KG.
    IS_KG: The bare-form includes vowel epenthesis, therefore the last inserted vowel drope
    during suffixation. e.g. Çelenk

    - Returns: true if flags list contains IS_KG.
    */
    public func endingKChangesIntoG() -> Bool{
        return self.__flags.contains("IS_KG")
    }

    /**
    The isExceptional method returns true if flags list contains IS_EX.
    IS_EX: This tag defines exception words. e.g. Delikanlı

    - Returns: true if flags list contains IS_EX.
    */
    public func isExceptional() -> Bool{
        return self.__flags.contains("IS_EX")
    }

    /**
    The duplicatesDuringSuffixation method returns true if flags list contains IS_ST.
    IS_ST: The second consonant of the bare-form undergoes a resyllabification. e.g. His

    - Returns: true if flags list contains IS_ST.
    */
    public func duplicatesDuringSuffixation() -> Bool{
        return self.__flags.contains("IS_ST")
    }

    /**
    The duplicatesAndNotDuplicatesDuringSuffixation method returns true if flags list contains IS_STT.
    IS_STT: The second consonant of the bare-form undergoes a resyllabification. e.g. His

    - Returns: true if flags list contains IS_STT.
    */
    public func duplicatesAndNotDuplicatesDuringSuffixation() -> Bool{
        return self.__flags.contains("IS_STT")
    }

    /**
    The lastIdropsDuringSuffixation method returns true if flags list contains IS_UD.
    IS_UD: The bare-form includes vowel epenthesis, therefore the last inserted vowel drops during suffixation.
    e.g. Boyun

    - Returns: true if flags list contains IS_UD.
    */
    public func lastIdropsDuringSuffixation() -> Bool{
        return self.__flags.contains("IS_UD")
    }

    /**
    The lastIDropsAndNotDropDuringSuffixation method returns true if flags list contains IS_UDD.
    IS_UDD: The bare-form includes vowel epenthesis, therefore the last inserted vowel can (or can not) drop during
    suffixation. e.g. Kadir

    - Returns: true if flags list contains IS_UDD.
    */
    public func lastIDropsAndNotDropDuringSuffixation() -> Bool{
        return self.__flags.contains("IS_UDD")
    }

    /**
    The takesRelativeSuffixKi method returns true if flags list contains IS_KI.
    IS_KI: The word can take a suffix such as "ki". e.g. Önce

    - Returns: true if flags list contains IS_KI.
    */
    public func takesRelativeSuffixKi() -> Bool{
        return self.__flags.contains("IS_KI")
    }

    /**
    The takesRelativeSuffixKu method returns true if flags list contains IS_KU.
    IS_KU: The word can take a suffix such as "kü". e.g. Bugün

    - Returns: true if flags list contains IS_KU.
    */
    public func takesRelativeSuffixKu() -> Bool{
        return self.__flags.contains("IS_KU")
    }

    /**
    The consonantSMayInsertedDuringPossesiveSuffixation method returns true if flags list contains IS_SII.

    - Returns: true if flags list contains IS_SII.
    */
    public func consonantSMayInsertedDuringPossesiveSuffixation() -> Bool{
        return self.__flags.contains("IS_SII")
    }

    /**
    The lastIdropsDuringPassiveSuffixation method returns true if flags list contains F_UD.
    F_UD: The bare-form includes vowel epenthesis, therefore the last "ı"
    drops during passive suffixation. e.g. Çağır

    - Returns: true if flags list contains F_UD.
    */
    public func lastIdropsDuringPassiveSuffixation() -> Bool{
        return self.__flags.contains("F_UD")
    }

    /**
    The vowelAChangesToIDuringYSuffixation method returns true if flags list contains F_GUD.
    F_GUD: The verb bare-form includes vowel reduction, the last vowel "a" of the bare-form is replaced with "ı"
    e.g. Buzağıla

    - Returns: true if flags list contains F_GUD.
    */
    public func vowelAChangesToIDuringYSuffixation() -> Bool{
        return self.__flags.contains("F_GUD")
    }

    /**
    The vowelEChangesToIDuringYSuffixation method returns true if flags list contains F_GUDO.
    F_GUDO: The verb bare-form includes viwel reduction, the last vowel "e" of the
    bare-form is replaced with "i". e.g. Ye

    - Returns: true if flags list contains F_GUDO.
    */
    public func vowelEChangesToIDuringYSuffixation() -> Bool{
        return self.__flags.contains("F_GUDO")
    }

    /**
    The takesSuffixIRAsAorist method returns true if flags list contains F_GIR.
    F_GIR: The bare-form of the word takes "ir" suffix. e.g. Geç

    - Returns: true if flags list contains F_GIR.
    */
    public func takesSuffixIRAsAorist() -> Bool{
        return !self.__flags.contains("F_GIR")
    }

    /**
    The takesSuffixDIRAsFactitive method returns true if flags list contains F_DIR.
    F_DIR: The bare-form of the word takes "tır" suffix. e.g. Daral

    - Returns: true if flags list contains F_DIR.
    */
    public func takesSuffixDIRAsFactitive() -> Bool{
        return !self.__flags.contains("F_DIR")
    }

    /**
    The showsSuRegularities method returns true if flags list contains IS_SU.

    - Returns: true if flags list contains IS_SU.
    */
    public func showsSuRegularities() -> Bool{
        return self.__flags.contains("IS_SU")
    }

    /**
    The containsFlag method returns true if flags list contains flag.

    - Returns: true if flags list contains flag.
    */
    public func containsFlag(flag: String) -> Bool{
        return self.__flags.contains(flag)
    }

    public override func description() -> String {
        var result : String = super.description()
        for flag in self.__flags{
            result = result + " " + flag
        }
        return result
    }
}

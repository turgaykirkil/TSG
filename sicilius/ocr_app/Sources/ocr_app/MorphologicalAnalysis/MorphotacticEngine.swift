//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 21.04.2022.
//

import Foundation


public class MorphotacticEngine{
    
    /// resolveD resolves the D metamorpheme to 'd' or 't' depending on the root and current formationToCheck. It adds
    /// 'd' if the root is an abbreviation; 't' if the last phoneme is one of the "çfhkpsşt" (fıstıkçı şahap) or 'd'
    /// otherwise; 't' if the word is a number ending with 3, 4, 5, 40, 60, or 70 or 'd' otherwise.
    /// - Parameters:
    ///   - root: Root of the word
    ///   - formation: Formation is current status of the wordform in the current state of the finite state machine. It
    ///                  is always equal to formationToCheck except the case where there is an apostrophe after the
    ///                  formationToCheck such as (3').
    ///   - formationToCheck: FormationToCheck is current status of the wordform in the current state of the finite
    ///                         state machine except the apostrophe at the end if it exists.
    /// - Returns: Formation with added 'd' or 't' character.
    public static func resolveD(root: TxtWord, formation: String, formationToCheck: String) -> String{
        if root.isAbbreviation() {
            return formation + "d"
        }
        if Word.lastPhoneme(stem: formationToCheck) >= "0" && Word.lastPhoneme(stem: formationToCheck) <= "9" {
            switch Word.lastPhoneme(stem: formationToCheck) {
                case "3", "4", "5":
                    //3->3'tü, 5->5'ti, 4->4'tü
                    return formation + "t"
                case "0":
                    if root.getName().hasSuffix("40") || root.getName().hasSuffix("60") || root.getName().hasSuffix("70"){
                        //40->40'tı, 60->60'tı, 70->70'ti
                        return formation + "t"
                    } else {
                        //30->30'du, 50->50'ydi, 80->80'di
                        return formation + "d"
                    }
                default:
                    return formation + "d"
            }
        } else {
            if TurkishLanguage.isSertSessiz(ch: Word.lastPhoneme(stem: formationToCheck)) {
                //yap+DH->yaptı
                return formation + "t"
            } else {
                //sar+DH->sardı
                return formation + "d"
            }
        }
    }
    
    /// resolveA resolves the A metamorpheme to 'a' or 'e' depending on the root and current formationToCheck. It adds
    /// 'e' if the root is an abbreviation; 'a' if the last vowel is a back vowel (except words that do not obey vowel
    /// harmony during agglutination); 'e' if the last vowel is a front vowel (except words that do not obey vowel
    /// harmony during agglutination); 'a' if the word is a number ending with 6, 9, 10, 30, 40, 60, or 90 or 'e'
    /// otherwise.
    /// - Parameters:
    ///   - root: Root of the word
    ///   - formation: Formation is current status of the wordform in the current state of the finite state machine. It
    ///                  is always equal to formationToCheck except the case where there is an apostrophe after the
    ///                  formationToCheck such as (3').
    ///   - rootWord: True if the current word form is root form, false otherwise.
    ///   - formationToCheck: FormationToCheck is current status of the wordform in the current state of the finite
    ///                         state machine except the apostrophe at the end if it exists.
    /// - Returns: Formation with added 'a' or 'e' character.
    public static func resolveA(root: TxtWord, formation: String, rootWord: Bool, formationToCheck: String) -> String{
        if root.isAbbreviation() {
            return formation + "e"
        }
        if Word.lastVowel(stem: formationToCheck) >= "0" && Word.lastVowel(stem: formationToCheck) <= "9" {
            switch Word.lastVowel(stem: formationToCheck) {
                case "6", "9":
                    //6'ya, 9'a
                    return formation + "a"
                case "0":
                    if root.getName().hasSuffix("10") || root.getName().hasSuffix("30") || root.getName().hasSuffix("40") || root.getName().hasSuffix("60") || root.getName().hasSuffix("90"){
                        //10'a, 30'a, 40'a, 60'a, 90'a
                        return formation + "a"
                    } else {
                        //20'ye, 50'ye, 80'e, 70'e
                        return formation + "e"
                    }
                default:
                    //3'e, 8'e, 4'e, 2'ye
                    return formation + "e"
            }
        }
        if TurkishLanguage.isBackVowel(ch: Word.lastVowel(stem: formationToCheck)) {
            if (root.notObeysVowelHarmonyDuringAgglutination() && rootWord) {
                //alkole, anormale
                return formation + "e"
            } else {
                //sakala, kabala
                return formation + "a"
            }
        }
        if TurkishLanguage.isFrontVowel(ch: Word.lastVowel(stem: formationToCheck)) {
            if root.notObeysVowelHarmonyDuringAgglutination() && rootWord {
                //faika, halika
                return formation + "a"
            } else {
                //kediye, eve
                return formation + "e"
            }
        }
        if root.isNumeral() || root.isFraction() || root.isReal() {
            if root.getName().hasSuffix("6") || root.getName().hasSuffix("9") || root.getName().hasSuffix("10") || root.getName().hasSuffix("30") || root.getName().hasSuffix("40") || root.getName().hasSuffix("60") || root.getName().hasSuffix("90") {
                return formation + "a"
            } else {
                return formation + "e"
            }
        }
        return formation
    }
    
    /// resolveH resolves the H metamorpheme to 'ı', 'i', 'u' or 'ü', depending on the  current formationToCheck, root,
    /// and formation. It adds 'i' if the root is an abbreviation; 'ü' if the  character before the last vowel is
    /// front rounded (or back rounded when the root word does not obey vowel harmony during agglutination); 'i' if the
    /// character before the last vowel is front unrounded; 'u' if the character before the  last vowel is back rounded;
    /// 'ı' if the character before the last vowel is back unrounded (or front unrounded when the root word does not obey
    /// vowel harmony during agglutination); 'ı' if the word is a  number ending with 6, 40, 60 or 90; 'ü' if the word
    /// is a number ending with 3, 4, or 00; 'u' if the word is a number ending with 9, 10, or 30; 'i' otherwise for
    /// numbers. Special case for 'Hyor' suffix is handled with resolveHforSpecialCaseTenseSuffix method.
    /// - Parameters:
    ///   - root: Root of the word
    ///   - formation: Formation is current status of the wordform in the current state of the finite state machine. It
    ///                  is always equal to formationToCheck except the case where there is an apostrophe after the
    ///                  formationToCheck such as (3').
    ///   - beginningOfSuffix: True if H appears in the beginning of the suffix, false otherwise.
    ///   - specialCaseTenseSuffix: True if the suffix is 'Hyor', false otherwise.
    ///   - rootWord: True if the current word form is root form, false otherwise.
    ///   - formationToCheck: FormationToCheck is current status of the word form in the current state of the finite
    ///                         state machine except the apostrophe at the end if it exists.
    /// - Returns: Formation with possibly last character dropped and 'ı', 'i', 'u' or 'ü' character added.
    public static func resolveH(root: TxtWord, formation: String, beginningOfSuffix: Bool, specialCaseTenseSuffix: Bool, rootWord: Bool, formationToCheck: String) -> String{
        if root.isAbbreviation(){
            return formation + "i"
        }
        if beginningOfSuffix && TurkishLanguage.isVowel(ch: Word.lastPhoneme(stem: formationToCheck)) && !specialCaseTenseSuffix {
            return formation;
        }
        if specialCaseTenseSuffix {
            //eğer ek Hyor eki ise,
            if rootWord {
                if root.vowelAChangesToIDuringYSuffixation() {
                    if TurkishLanguage.isFrontRoundedVowel(ch: Word.beforeLastVowel(stem: formationToCheck)) {
                        //büyülüyor, bölümlüyor, çözümlüyor, döşüyor
                        return formation.prefix(formation.count - 1) + "ü"
                    }
                    if (TurkishLanguage.isFrontUnroundedVowel(ch: Word.beforeLastVowel(stem: formationToCheck))) {
                        //adresliyor, alevliyor, ateşliyor, bekliyor
                        return formation.prefix(formation.count - 1) + "i"
                    }
                    if (TurkishLanguage.isBackRoundedVowel(ch: Word.beforeLastVowel(stem: formationToCheck))) {
                        //buğuluyor, bulguluyor, çamurluyor, aforozluyor
                        return formation.prefix(formation.count - 1) + "u"
                    }
                    if (TurkishLanguage.isBackUnroundedVowel(ch: Word.beforeLastVowel(stem: formationToCheck))) {
                        //açıklıyor, çalkalıyor, gazlıyor, gıcırdıyor
                        return formation.prefix(formation.count - 1) + "ı"
                    }
                }
            }
            if TurkishLanguage.isVowel(ch: Word.lastPhoneme(stem: formationToCheck)) {
                if TurkishLanguage.isFrontRoundedVowel(ch: Word.beforeLastVowel(stem: formationToCheck)) {
                    return formation.prefix(formation.count - 1) + "ü"
                }
                if TurkishLanguage.isFrontUnroundedVowel(ch: Word.beforeLastVowel(stem: formationToCheck)) {
                    return formation.prefix(formation.count - 1) + "i"
                }
                if TurkishLanguage.isBackRoundedVowel(ch: Word.beforeLastVowel(stem: formationToCheck)) {
                    return formation.prefix(formation.count - 1) + "u"
                }
                if TurkishLanguage.isBackUnroundedVowel(ch: Word.beforeLastVowel(stem: formationToCheck)) {
                    return formation.prefix(formation.count - 1) + "ı"
                }
            }
        }
        if TurkishLanguage.isFrontRoundedVowel(ch: Word.lastVowel(stem: formationToCheck)) || (TurkishLanguage.isBackRoundedVowel(ch: Word.lastVowel(stem: formationToCheck)) && root.notObeysVowelHarmonyDuringAgglutination()) {
            return formation + "ü"
        }
        if (TurkishLanguage.isFrontUnroundedVowel(ch: Word.lastVowel(stem: formationToCheck)) && !root.notObeysVowelHarmonyDuringAgglutination()) || ((Word.lastVowel(stem: formationToCheck) == "a" || Word.lastVowel(stem: formationToCheck) == "â") && root.notObeysVowelHarmonyDuringAgglutination()) {
            return formation + "i"
        }
        if TurkishLanguage.isBackRoundedVowel(ch: Word.lastVowel(stem: formationToCheck)) {
            return formation + "u"
        }
        if TurkishLanguage.isBackUnroundedVowel(ch: Word.lastVowel(stem: formationToCheck)) || (TurkishLanguage.isFrontUnroundedVowel(ch: Word.lastVowel(stem: formationToCheck)) && root.notObeysVowelHarmonyDuringAgglutination()){
            return formation + "ı"
        }
        if root.isNumeral() || root.isFraction() || root.isReal() {
            if root.getName().hasSuffix("6") || root.getName().hasSuffix("40") || root.getName().hasSuffix("60") || root.getName().hasSuffix("90") {
                //6'yı, 40'ı, 60'ı
                return formation + "ı"
            } else {
                if root.getName().hasSuffix("3") || root.getName().hasSuffix("4") || root.getName().hasSuffix("00") {
                    //3'ü, 4'ü, 100'ü
                    return formation + "ü"
                } else {
                    if root.getName().hasSuffix("9") || root.getName().hasSuffix("10") || root.getName().hasSuffix("30") {
                        //9'u, 10'u, 30'u
                        return formation + "u"
                    } else {
                        //2'yi, 5'i, 8'i
                        return formation + "i"
                    }
                }
            }
        }
        return formation
    }
    
    /**
     * The resolveC method takes a {@link String} formation as an input. If the last phoneme is on of the "çfhkpsşt", it
     * concatenates given formation with 'ç', if not it concatenates given formation with 'c'.
        - Parameters:
            - formation: {@link String} input.
        - Returns: resolved String.
     */
    public static func resolveC(formation: String, formationToCheck: String) -> String{
        if TurkishLanguage.isSertSessiz(ch: Word.lastPhoneme(stem: formationToCheck)) {
            return formation + "ç"
        } else {
            return formation + "c"
        }
    }
    
    /**
     * The resolveS method takes a {@link String} formation as an input. It then concatenates given formation with 's'.
        - Parameters:
            - formation: {@link String} input.
        - Returns: resolved String.
     */
    public static func resolveS(formation: String) -> String{
        return formation + "s"
    }
    
    /**
     * The resolveSh method takes a {@link String} formation as an input. If the last character is a vowel, it concatenates
     * given formation with ş, if the last character is not a vowel, and not 't' it directly returns given formation, but if it
     * is equal to 't', it transforms it to 'd'.
        - Parameters:
            - formation: {@link String} input.
        - Returns: resolved String.
     */
    public static func resolveSh(formation: String) -> String{
        if TurkishLanguage.isVowel(ch: Word.charAt(s: formation, i: formation.count - 1)) {
            return formation + "ş"
        } else {
            if Word.charAt(s: formation, i: formation.count - 1) != "t"{
                return formation;
            } else {
                return formation.prefix(formation.count - 1) + "d"
            }
        }
    }

}

//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 7.03.2021.
//

import Foundation


public class FsmParse: MorphologicalParse, NSCopying{
    
    private var _suffixList: [FsmState] = []
    private var _formList: [String] = []
    private var _transitionList: [String] = []
    private var _withList: [String] = []
    private var _initialPos: String? = nil
    private var _pos: String? = nil
    private var _form: String = ""
    private var _verbAgreement: String? = nil
    private var _possesiveAgreement: String? = nil
    
    /**
     * A constructor of {@link FsmParse} class which takes a {@link Word} as an input and assigns it to root variable.
        - Parameters:
            - root: {@link Word} input.
     */
    public init(root: Word) {
        super.init()
        self.root = root
    }
    
    /**
     * Another constructor of {@link FsmParse} class which takes an {@link Integer} number and a {@link State} as inputs.
     * First, it creates a {@link TxtWord} with given number and adds flag to this number as IS_SAYI and initializes root variable with
     * number {@link TxtWord}. It also initializes form with root's name, pos and initialPos with given {@link State}'s POS, creates 4 new
     * {@link ArrayList} suffixList, formList, transitionList and withList and adds given {@link State} to suffixList, form to
     * formList.
        - Parameters:
            - number :    {@link Integer} input.
            - startState: {@link State} input.
     */
    public init(number: Int, startState: FsmState){
        super.init()
        let num: TxtWord = TxtWord(name: "" + String(number))
        num.addFlag(flag: "IS_SAYI")
        root = num
        _form = root.getName()
        _pos = startState.getPos()
        _initialPos = startState.getPos()
        _suffixList.append(startState)
        _formList.append(_form)
    }
    
    /**
     * Another constructor of {@link FsmParse} class which takes an {@link Double} number and a {@link State} as inputs.
     * First, it creates a {@link TxtWord} with given number and adds flag to this number as IS_SAYI and initializes root variable with
     * number {@link TxtWord}. It also initializes form with root's name, pos and initialPos with given {@link State}'s POS, creates 4 new
     * {@link ArrayList} suffixList, formList, transitionList and withList and adds given {@link State} to suffixList, form to
     * formList.
        - Parameters:
            - number :    {@link Double} input.
            - startState: {@link State} input.
     */
    public init(number: Double, startState: FsmState){
        super.init()
        let num: TxtWord = TxtWord(name: "" + String(number))
        num.addFlag(flag: "IS_SAYI")
        root = num
        _form = root.getName()
        _pos = startState.getPos()
        _initialPos = startState.getPos()
        _suffixList.append(startState)
        _formList.append(_form)
    }
    
    /**
     * Another constructor of {@link FsmParse} class which takes a {@link String} punctuation and a {@link State} as inputs.
     * First, it creates a {@link TxtWord} with given punctuation and initializes root variable with this {@link TxtWord}.
     * It also initializes form with root's name, pos and initialPos with given {@link State}'s POS, creates 4 new
     * {@link ArrayList} suffixList, formList, transitionList and withList and adds given {@link State} to suffixList, form to
     * formList.
        - Parameters:
            - punctuation {@link String} input.
            - startState  {@link State} input.
     */
    public init(punctuation: String, startState: FsmState){
        super.init()
        root = TxtWord(name: punctuation)
        _form = root.getName()
        _pos = startState.getPos()
        _initialPos = startState.getPos()
        _suffixList.append(startState)
        _formList.append(_form)
    }
    
    /**
     * Another constructor of {@link FsmParse} class which takes a {@link TxtWord} root and a {@link State} as inputs.
     * First, initializes root variable with this {@link TxtWord}. It also initializes form with root's name, pos and
     * initialPos with given {@link State}'s POS, creates 4 new {@link ArrayList} suffixList, formList, transitionList
     * and withList and adds given {@link State} to suffixList, form to formList.
        - Parameters:
            - root: {@link TxtWord} input.
            - startState: {@link State} input.
     */
    public init(root: TxtWord, startState: FsmState){
        super.init()
        self.root = root
        _form = root.getName()
        _pos = startState.getPos()
        _initialPos = startState.getPos()
        _suffixList.append(startState)
        _formList.append(_form)
    }
    
    /**
     * The constructInflectionalGroups method initially calls the transitionList method and assigns the resulting {@link String}
     * to the parse variable and creates a new {@link ArrayList} as iGs. If parse {@link String} contains a derivational boundary
     * it adds the substring starting from the 0 to the index of derivational boundary to the iGs. If it does not contain a DB,
     * it directly adds parse to the iGs. Then, creates and initializes new {@link ArrayList} as inflectionalGroups and fills with
     * the items of iGs.
     */
    public func constructInflectionalGroups(){
        var parse: String = self.transitionList()
        var iGs : [String] = []
        while parse.contains("^DB+") {
            iGs.append(String(parse[..<parse.firstIndex(of: "^")!]))
            parse = String(parse[parse.index(after: parse.firstIndex(of: "+")!)...])
        }
        iGs.append(parse)
        inflectionalGroups.append(InflectionalGroup(IG: String(iGs[0][iGs[0].index(after: iGs[0].firstIndex(of: "+")!)...])))
        for i in 1..<iGs.count {
            inflectionalGroups.append(InflectionalGroup(IG: iGs[i]))
        }
    }
    
    /**
     * Getter for the verbAgreement variable.
        - Returns: The verbAgreement variable.
     */
    public func getVerbAgreement() -> String?{
        return _verbAgreement
    }
    
    /**
     * Getter for the getPossesiveAgreement variable.
        - Returns: The possesiveAgreement variable.
     */
    public func getPossessiveAgreement() -> String?{
        return _possesiveAgreement
    }
    
    /**
     * The setAgreement method takes a {@link String} transitionName as an input and if it is one of the A1SG, A2SG, A3SG,
     * A1PL, A2PL or A3PL it assigns transitionName input to the verbAgreement variable. Or if it is ine of the PNON, P1SG, P2SG,P3SG,
     * P1PL, P2PL or P3PL it assigns transitionName input to the possesiveAgreement variable.
        - Parameters:
            - transitionName: {@link String} input.
     */
    public func setAgreement(transitionName: String?){
        if transitionName != nil && (transitionName == "A1SG" || transitionName == "A2SG" || transitionName == "A3SG" || transitionName == "A1PL" || transitionName == "A2PL" || transitionName == "A3PL") {
            _verbAgreement = transitionName
        }
        if transitionName != nil && (transitionName == "PNON" || transitionName == "P1SG" || transitionName == "P2SG" || transitionName == "P3SG" || transitionName == "P1PL" || transitionName == "P2PL" || transitionName == "P3PL") {
            _possesiveAgreement = transitionName
        }
    }
    
    /**
     * The getLastLemmaWithTag method takes a String input pos as an input. If given pos is an initial pos then it assigns
     * root to the lemma, and assign null otherwise.  Then, it loops i times where i ranges from 1 to size of the formList,
     * if the item at i-1 of transitionList is not null and contains a derivational boundary with pos but not with ZERO,
     * it assigns the ith item of formList to lemma.
        - Parameters:
            - pos: {@link String} input.
        - Returns: String output lemma.
     */
    public func getLastLemmaWithTag(pos: String) -> String?{
        var lemma: String?
        if _initialPos != nil && _initialPos == pos {
            lemma = root.getName()
        } else {
            lemma = nil
        }
        for i in 1..<_formList.count {
            if _transitionList[i - 1].contains("^DB+" + pos) && !_transitionList[i - 1].contains("^DB+" + pos + "+ZERO") {
                lemma = _formList[i]
            }
        }
        return lemma
    }
    
    /**
     * The getLastLemma method initially assigns root as lemma. Then, it loops i times where i ranges from 1 to size of the formList,
     * if the item at i-1 of transitionList is not null and contains a derivational boundary, it assigns the ith item of formList to lemma.
        - Returns: String output lemma.
     */
    public func getLastLemma() -> String{
        var lemma : String = root.getName()
        for i in 1..<_formList.count {
            if _transitionList[i - 1].contains("^DB+") {
                lemma = _formList[i]
            }
        }
        return lemma
    }
    
    /**
     * The addSuffix method takes 5 different inputs; {@link State} suffix, {@link String} form, transition, with and toPos.
     * If the pos of given input suffix is not null, it then assigns it to the pos variable. If the pos of the given suffix
     * is null but given toPos is not null than it assigns toPos to pos variable. At the end, it adds suffix to the suffixList,
     * form to the formList, transition to the transitionList and if given with is not 0, it is also added to withList.
        - Parameters:
            - suffix:     {@link State} input.
            - form:       {@link String} input.
            - transition: {@link String} input.
            -  with:       {@link String} input.
            - toPos:      {@link String} input.
     */
    public func addSuffix(suffix: FsmState, form: String, transition: String?, with: String, toPos: String?){
        if suffix.getPos() != nil {
            _pos = suffix.getPos()!
        } else {
            if toPos != nil {
                _pos = toPos!
            }
        }
        _suffixList.append(suffix)
        _formList.append(form)
        _transitionList.append(transition ?? "")
        if with != "0" {
            _withList.append(with)
        }
        self._form = form
    }
    
    /**
     * Getter for the form variable.
        - Returns: The form variable.
     */
    public func getSurfaceForm() -> String{
        return _form
    }
    
    /**
     * The getStartState method returns the first item of suffixList {@link ArrayList}.
        - Returns: The first item of suffixList {@link ArrayList}.
     */
    public func getStartState() -> FsmState{
        return _suffixList[0]
    }
    
    /**
     * Getter for the pos variable.
        - Returns: The pos variable.
     */
    public func getFinalPos() -> String?{
        return _pos
    }
    
    /**
     * Getter for the initialPos variable.
     - Returns: Tthe initialPos variable.
     */
    public func getInitialPos() -> String?{
        return _initialPos
    }
    
    /**
     * The setForm method takes a {@link String} name as an input and assigns it to the form variable, then it removes the first item
     * of formList {@link ArrayList} and adds the given name to the formList.
        - Parameters:
            - name: String input to set form.
     */
    public func setForm(name: String){
        _form = name
        _formList.remove(at: 0)
        _formList.append(name)
    }
    
    /**
     * The getFinalSuffix method returns the last item of suffixList {@link ArrayList}.
        - Returns: The last item of suffixList {@link ArrayList}.
     */
    public func getFinalSuffix() -> FsmState{
        return _suffixList.last!
    }
    
    /**
     * The overridden copy method creates a new {@link FsmParse} abject with root variable and initializes variables form, pos,
     * initialPos, verbAgreement, possesiveAgreement, and also the {@link ArrayList}s suffixList, formList, transitionList and withList.
     * Then returns newly created and cloned {@link FsmParse} object.
     - Returns: FsmParse object.
     */
    public func copy(with zone: NSZone? = nil) -> Any {
        let p : FsmParse = FsmParse(root: root)
        p._form = _form;
        p._pos = _pos;
        p._initialPos = _initialPos;
        p._verbAgreement = _verbAgreement;
        p._possesiveAgreement = _possesiveAgreement;
        p._suffixList = []
        for i in 0..<_suffixList.count {
            p._suffixList.append(_suffixList[i])
        }
        p._formList = []
        for i in 0..<_formList.count {
            p._formList.append(_formList[i])
        }
        p._transitionList = []
        for i in 0..<_transitionList.count {
            p._transitionList.append(_transitionList[i])
        }
        p._withList = []
        for i in 0..<_withList.count {
            p._withList.append(_withList[i])
        }
        return p
    }
    
    /**
     * The headerTransition method gets the first item of formList and checks for cases;
     * <p>
     * If it is &lt;DOC&gt;, it returns &lt;DOC&gt;+BDTAG which indicates the beginning of a document.
     * If it is &lt;/DOC&gt;, it returns &lt;/DOC&gt;+EDTAG which indicates the ending of a document.
     * If it is &lt;TITLE&gt;, it returns &lt;TITLE&gt;+BTTAG which indicates the beginning of a title.
     * If it is &lt;/TITLE&gt;, it returns &lt;/TITLE&gt;+ETTAG which indicates the ending of a title.
     * If it is &lt;S&gt;, it returns &lt;S&gt;+BSTAG which indicates the beginning of a sentence.
     * If it is &lt;/S&gt;, it returns &lt;/S&gt;+ESTAG which indicates the ending of a sentence.
        - Returns: Corresponding tags of the headers and an empty {@link String} if any case does not match.
     */
    public func headerTransition() -> String{
        if _formList[0] == "<DOC>" {
            return "<DOC>+BDTAG"
        }
        if _formList[0] == "</DOC>" {
            return "</DOC>+EDTAG"
        }
        if _formList[0] == "<TITLE>" {
            return "<TITLE>+BTTAG"
        }
        if _formList[0] == "</TITLE>" {
            return "</TITLE>+ETTAG"
        }
        if _formList[0] == "<S>" {
            return "<S>+BSTAG"
        }
        if _formList[0] == "</S>" {
            return "</S>+ESTAG"
        }
        return "";
    }
    
    /**
     * The pronounTransition method gets the first item of formList and checks for cases;
     * <p>
     * If it is "kendi", it returns kendi+PRON+REFLEXP which indicates a reflexive pronoun.
     * If it is one of the "hep, öbür, topu, öteki, kimse, hiçbiri, tümü, çoğu, hepsi, herkes, başkası, birçoğu, birçokları, biri, birbirleri, birbiri, birkaçı, böylesi, diğeri, cümlesi, bazı, kimi", it returns
     * +PRON+QUANTP which indicates a quantitative pronoun.
     * If it is one of the "o, bu, şu" and if it is "o" it also checks the first item of suffixList and if it is a PronounRoot(DEMONS),
     * it returns +PRON+DEMONSP which indicates a demonstrative pronoun.
     * If it is "ben", it returns +PRON+PERS+A1SG+PNON which indicates a 1st person singular agreement.
     * If it is "sen", it returns +PRON+PERS+A2SG+PNON which indicates a 2nd person singular agreement.
     * If it is "o" and the first item of suffixList, if it is a PronounRoot(PERS), it returns +PRON+PERS+A3SG+PNON which
     * indicates a 3rd person singular agreement.
     * If it is "biz", it returns +PRON+PERS+A1PL+PNON which indicates a 1st person plural agreement.
     * If it is "siz", it returns +PRON+PERS+A2PL+PNON which indicates a 2nd person plural agreement.
     * If it is "onlar" and the first item of suffixList, if it is a PronounRoot(PERS), it returns o+PRON+PERS+A3PL+PNON which
     * indicates a 3rd person plural agreement.
     * If it is one of the "nere, ne, kim, hangi", it returns +PRON+QUESP which indicates a question pronoun.
        - Returns: Corresponding transitions of pronouns and an empty {@link String} if any case does not match.
     */
    public func pronounTransition() -> String{
        if _formList[0] == "kendi" {
            return "kendi+PRON+REFLEXP"
        }
        if _formList[0] == "hep" || _formList[0] == "öbür" || _formList[0] == "topu" || _formList[0] == "öteki" || _formList[0] == "kimse" || _formList[0] == "hiçbiri" || _formList[0] == "tümü" || _formList[0] == "çoğu" || _formList[0] == "hepsi" || _formList[0] == "herkes" || _formList[0] == "başkası" || _formList[0] == "birçoğu" || _formList[0] == "birçokları" || _formList[0] == "birbiri" || _formList[0] == "birbirleri" || _formList[0] == "biri" || _formList[0] == "birkaçı" || _formList[0] == "böylesi" || _formList[0] == "diğeri" || _formList[0] == "cümlesi" || _formList[0] == "bazı" || _formList[0] == "kimi" {
            return _formList[0] + "+PRON+QUANTP"
        }
        if _formList[0] == "o" && _suffixList[0].getName() == "PronounRoot(DEMONS)" || _formList[0] == "bu" || _formList[0] == "şu" {
            return _formList[0] + "+PRON+DEMONSP"
        }
        if _formList[0] == "ben" {
            return _formList[0] + "+PRON+PERS+A1SG+PNON"
        }
        if _formList[0] == "sen" {
            return _formList[0] + "+PRON+PERS+A2SG+PNON"
        }
        if _formList[0] == "o" && _suffixList[0].getName() == "PronounRoot(PERS)" {
            return _formList[0] + "+PRON+PERS+A3SG+PNON"
        }
        if _formList[0] == "biz" {
            return _formList[0] + "+PRON+PERS+A1PL+PNON"
        }
        if _formList[0] == "siz" {
            return _formList[0] + "+PRON+PERS+A2PL+PNON"
        }
        if _formList[0] == "onlar" {
            return "o+PRON+PERS+A3PL+PNON"
        }
        if _formList[0] == "nere" || _formList[0] == "ne" || _formList[0] == "kaçı" || _formList[0] == "kim" || _formList[0] == "hangi" {
            return _formList[0] + "+PRON+QUESP"
        }
        return ""
    }
    
    /**
     * The transitionList method first creates an empty {@link String} result, then gets the first item of suffixList and checks for cases;
     * <p>
     * If it is one of the "NominalRoot, NominalRootNoPossesive, CompoundNounRoot, NominalRootPlural", it assigns concatenation of first
     * item of formList and +NOUN to the result String.
     * Ex : Birincilik
     * <p>
     * If it is one of the "VerbalRoot, PassiveHn", it assigns concatenation of first item of formList and +VERB to the result String.
     * Ex : Başkalaştı
     * <p>
     * If it is "CardinalRoot", it assigns concatenation of first item of formList and +NUM+CARD to the result String.
     * Ex : Onuncu
     * <p>
     * If it is "FractionRoot", it assigns concatenation of first item of formList and NUM+FRACTION to the result String.
     * Ex : 1/2
     * <p>
     * If it is "TimeRoot", it assigns concatenation of first item of formList and +TIME to the result String.
     * Ex : 14:28
     * <p>
     * If it is "RealRoot", it assigns concatenation of first item of formList and +NUM+REAL to the result String.
     * Ex : 1.2
     * <p>
     * If it is "Punctuation", it assigns concatenation of first item of formList and +PUNC to the result String.
     * Ex : ,
     * <p>
     * If it is "Hashtag", it assigns concatenation of first item of formList and +HASHTAG to the result String.
     * Ex : #
     * <p>
     * If it is "DateRoot", it assigns concatenation of first item of formList and +DATE to the result String.
     * Ex : 11/06/2018
     * <p>
     * If it is "RangeRoot", it assigns concatenation of first item of formList and +RANGE to the result String.
     * Ex : 3-5
     * <p>
     * If it is "Email", it assigns concatenation of first item of formList and +EMAIL to the result String.
     * Ex : abc@
     * <p>
     * If it is "PercentRoot", it assigns concatenation of first item of formList and +PERCENT to the result String.
     * Ex : %12.5
     * <p>
     * If it is "DeterminerRoot", it assigns concatenation of first item of formList and +DET to the result String.
     * Ex : Birtakım
     * <p>
     * If it is "ConjunctionRoot", it assigns concatenation of first item of formList and +CONJ to the result String.
     * Ex : Ama
     * <p>
     * If it is "AdverbRoot", it assigns concatenation of first item of formList and +ADV to the result String.
     * Ex : Acilen
     * <p>
     * If it is "ProperRoot", it assigns concatenation of first item of formList and +NOUN+PROP to the result String.
     * Ex : Ahmet
     * <p>
     * If it is "HeaderRoot", it assigns the result of the headerTransition method to the result String.
     * Ex : &lt;DOC&gt;
     * <p>
     * If it is "InterjectionRoot", it assigns concatenation of first item of formList and +INTERJ to the result String.
     * Ex : Hey
     * <p>
     * If it is "DuplicateRoot", it assigns concatenation of first item of formList and +DUP to the result String.
     * Ex : Allak
     * <p>
     * If it is "CodeRoot", it assigns concatenation of first item of formList and +CODE to the result String.
     * Ex : 5000-WX
     * <p>
     * If it is "MetricRoot", it assigns concatenation of first item of formList and +METRIC to the result String.
     * Ex : 6cmx12cm
     * <p>
     * If it is "QuestionRoot", it assigns concatenation of first item of formList and +QUES to the result String.
     * Ex : Mı
     * <p>
     * If it is "PostP", and the first item of formList is one of the "karşı, ilişkin, göre, kadar, ait, yönelik, rağmen, değin,
     * dek, doğru, karşın, dair, atfen, binaen, hitaben, istinaden, mahsuben, mukabil, nazaran", it assigns concatenation of first
     * item of formList and +POSTP+PCDAT to the result String.
     * Ex : İlişkin
     * <p>
     * If it is "PostP", and the first item of formList is one of the "sonra, önce, beri, fazla, dolayı, itibaren, başka,
     * çok, evvel, ötürü, yana, öte, aşağı, yukarı, dışarı, az, gayrı", it assigns concatenation of first
     * item of formList and +POSTP+PCABL to the result String.
     * Ex : Başka
     * <p>
     * If it is "PostP", and the first item of formList is "yanısıra", it assigns concatenation of first
     * item of formList and +POSTP+PCGEN to the result String.
     * Ex : Yanısıra
     * <p>
     * If it is "PostP", and the first item of formList is one of the "birlikte, beraber", it assigns concatenation of first
     * item of formList and +PPOSTP+PCINS to the result String.
     * Ex : Birlikte
     * <p>
     * If it is "PostP", and the first item of formList is one of the "aşkın, takiben", it assigns concatenation of first
     * item of formList and +POSTP+PCACC to the result String.
     * Ex : Takiben
     * <p>
     * If it is "PostP", it assigns concatenation of first item of formList and +POSTP+PCNOM to the result String.
     * <p>
     * If it is "PronounRoot", it assigns result of the pronounTransition method to the result String.
     * Ex : Ben
     * <p>
     * If it is "OrdinalRoot", it assigns concatenation of first item of formList and +NUM+ORD to the result String.
     * Ex : Altıncı
     * <p>
     * If it starts with "Adjective", it assigns concatenation of first item of formList and +ADJ to the result String.
     * Ex : Güzel
     * <p>
     * At the end, it loops through the formList and concatenates each item with result {@link String}.
        - Returns: String result accumulated with items of formList.
     */
    public func transitionList() -> String{
        var result : String = ""
        if _suffixList[0].getName() == "NominalRoot" || _suffixList[0].getName() == "NominalRootNoPossesive" || _suffixList[0].getName() == "CompoundNounRoot" || _suffixList[0].getName() == "NominalRootPlural" {
            result = _formList[0] + "+NOUN"
        } else {
            if _suffixList[0].getName().hasPrefix("VerbalRoot") || _suffixList[0].getName() == "PassiveHn" {
                result = _formList[0] + "+VERB"
            } else {
                if _suffixList[0].getName() == "CardinalRoot" {
                    result = _formList[0] + "+NUM+CARD"
                } else {
                    if _suffixList[0].getName() == "FractionRoot" {
                        result = _formList[0] + "+NUM+FRACTION"
                    } else {
                        if _suffixList[0].getName() == "TimeRoot" {
                            result = _formList[0] + "+TIME"
                        } else {
                            if _suffixList[0].getName() == "RealRoot" {
                                result = _formList[0] + "+NUM+REAL"
                            } else {
                                if _suffixList[0].getName() == "Punctuation" {
                                    result = _formList[0] + "+PUNC"
                                } else {
                                    if _suffixList[0].getName() == "Hashtag" {
                                        result = _formList[0] + "+HASHTAG"
                                    } else {
                                        if _suffixList[0].getName() == "DateRoot" {
                                            result = _formList[0] + "+DATE"
                                        } else {
                                            if _suffixList[0].getName() == "RangeRoot" {
                                                result = _formList[0] + "+RANGE"
                                            } else {
                                                if _suffixList[0].getName() == "Email" {
                                                    result = _formList[0] + "+EMAIL"
                                                } else {
                                                    if _suffixList[0].getName() == "PercentRoot" {
                                                        result = _formList[0] + "+PERCENT"
                                                    } else {
                                                        if _suffixList[0].getName() == "DeterminerRoot" {
                                                            result = _formList[0] + "+DET"
                                                        } else {
                                                            if _suffixList[0].getName() == "ConjunctionRoot" {
                                                                result = _formList[0] + "+CONJ"
                                                            } else {
                                                                if _suffixList[0].getName() == "AdverbRoot" {
                                                                    result = _formList[0] + "+ADV"
                                                                } else {
                                                                    if _suffixList[0].getName() == "ProperRoot" {
                                                                        result = _formList[0] + "+NOUN+PROP"
                                                                    } else {
                                                                        if _suffixList[0].getName() == "HeaderRoot" {
                                                                            result = headerTransition()
                                                                        } else {
                                                                            if _suffixList[0].getName() == "InterjectionRoot" {
                                                                                result = _formList[0] + "+INTERJ"
                                                                            } else {
                                                                                if _suffixList[0].getName() == "DuplicateRoot" {
                                                                                    result = _formList[0] + "+DUP"
                                                                                } else {
                                                                                    if _suffixList[0].getName() == "CodeRoot"{
                                                                                        result = _formList[0] + "+CODE"
                                                                                    } else {
                                                                                        if _suffixList[0].getName() == "MetricRoot"{
                                                                                            result = _formList[0] + "+METRIC"
                                                                                        } else {
                                                                                            if _suffixList[0].getName() == "QuestionRoot" {
                                                                                                result = "mi+QUES"
                                                                                            } else {
                                                                                                if _suffixList[0].getName() == "PostP" {
                                                                                                    if _formList[0] == "karşı" || _formList[0] == "ilişkin" || _formList[0] == "göre" || _formList[0] == "kadar" || _formList[0] == "ait" || _formList[0] == "yönelik" || _formList[0] == "rağmen" || _formList[0] == "değin" || _formList[0] == "dek" || _formList[0] == "doğru" || _formList[0] == "karşın" || _formList[0] == "dair" || _formList[0] == "atfen" || _formList[0] == "binaen" || _formList[0] == "hitaben" || _formList[0] == "istinaden" || _formList[0] == "mahsuben" || _formList[0] == "mukabil" || _formList[0] == "nazaran" {
                                                                                                        result = _formList[0] + "+POSTP+PCDAT"
                                                                                                    } else {
                                                                                                        if _formList[0] == "sonra" || _formList[0] == "önce" || _formList[0] == "beri" || _formList[0] == "fazla" || _formList[0] == "dolayı" || _formList[0] == "itibaren" || _formList[0] == "başka" || _formList[0] == "çok" || _formList[0] == "evvel" || _formList[0] == "ötürü" || _formList[0] == "yana" || _formList[0] == "öte" || _formList[0] == "aşağı" || _formList[0] == "yukarı" || _formList[0] == "dışarı" || _formList[0] == "az" || _formList[0] == "gayrı" {
                                                                                                            result = _formList[0] + "+POSTP+PCABL"
                                                                                                        } else {
                                                                                                            if _formList[0] == "yanısıra" {
                                                                                                                result = _formList[0] + "+POSTP+PCGEN"
                                                                                                            } else {
                                                                                                                if _formList[0] == "birlikte" || _formList[0] == "beraber" {
                                                                                                                    result = _formList[0] + "+POSTP+PCINS"
                                                                                                                } else {
                                                                                                                    if _formList[0] == "aşkın" || _formList[0] == "takiben" {
                                                                                                                        result = _formList[0] + "+POSTP+PCACC"
                                                                                                                    } else {
                                                                                                                        result = _formList[0] + "+POSTP+PCNOM"
                                                                                                                    }
                                                                                                                }
                                                                                                            }
                                                                                                        }
                                                                                                    }
                                                                                                } else {
                                                                                                    if _suffixList[0].getName().hasPrefix("PronounRoot") {
                                                                                                        result = pronounTransition()
                                                                                                    } else {
                                                                                                        if _suffixList[0].getName() == "OrdinalRoot" {
                                                                                                            result = _formList[0] + "+NUM+ORD"
                                                                                                        } else {
                                                                                                            if _suffixList[0].getName().hasPrefix("Adjective") {
                                                                                                                result = _formList[0] + "+ADJ"
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
        for transition in _transitionList {
            if transition != ""{
                if !transition.hasPrefix("^") {
                    result = result + "+" + transition
                } else {
                    result = result + transition
                }
            }
        }
        return result
    }
    
    /**
     * The suffixList method gets the first items of suffixList and formList and concatenates them with parenthesis and
     * assigns a String result. Then, loops through the formList and it the current ith item is not equal to previous
     * item it accumulates ith items of formList and suffixList to the result {@link String}.
        - Returns: Result {@link String} accumulated with the items of formList and suffixList.
     */
    public func suffixList() -> String{
        var result : String = _suffixList[0].getName() + "(" + _formList[0] + ")"
        for i in 1..<_formList.count {
            if _formList[i] != _formList[i - 1] {
                result = result + "+" + _suffixList[i].getName() + "(" + _formList[i] + ")"
            }
        }
        return result
    }
    
    /**
     * The withList method gets the root as a result {@link String} then loops through the withList and concatenates each item
     * with result {@link String}.
     - Returns: result {@link String} accumulated with items of withList.
     */
    public func withList() -> String{
        var result : String = root.getName()
        for aWith in _withList {
            result = result + "+" + aWith
        }
        return result
    }
    
    /**
     * Replace root word of the current parse with the new root word and returns the new word.
     * - Parameters:
     *     - newRoot: Replaced root word
       - Returns: Root word of the parse will be replaced with the newRoot and the resulting surface form is returned.
     */
    public func replaceRootWord(newRoot: TxtWord) -> String{
        var result : String = root.getName()
        for aWith in _withList {
            let transition = Transition(with: aWith)
            result = transition.makeTransition(root: newRoot, stem: result)
        }
        return result
    }

    public override func description() -> String{
        return transitionList()
    }

}

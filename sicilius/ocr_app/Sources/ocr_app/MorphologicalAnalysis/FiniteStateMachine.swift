//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 15.03.2021.
//

import Foundation

public class FiniteStateMachine: NSObject, XMLParserDelegate{
    
    private var states : [FsmState] = []
    private var transitions : Swift.Dictionary<FsmState, [Transition]> = [:]
    private var value: String = ""
    private var state: FsmState? = nil
    private var withName: String? = nil
    private var rootToPos: String? = nil
    private var toPos: String? = nil
    private var toState: FsmState? = nil
    private var first: Bool = true
    
    /// Default constructor for Finite State Machine. It reads turkish_finite_State_machine.xml
    public override init(){
        super.init()
        let url = Bundle.module.url(forResource: "turkish_finite_state_machine", withExtension: "xml")
        var parser : XMLParser = XMLParser(contentsOf: url!)!
        parser.delegate = self
        parser.parse()
        first = false
        parser = XMLParser(contentsOf: url!)!
        parser.delegate = self
        parser.parse()
    }
    
    /// Constructor reads the finite state machine in the given input file. DOMParser is used to parse the given file.
    /// Firstly it gets the document to parse.
    ///
    /// At the last step, by starting rootNode's first child, it gets all the transitionNodes and next states called toState,
    /// then continue with the nextSiblings. Also, if there is no possible toState, it prints this case and the causative states.
    /// - Parameter fileName: the resource file to read the finite state machine. Only files in resources folder are supported.
    public init(fileName: String){
        super.init()
        let url = Bundle.module.url(forResource: fileName, withExtension: "xml")
        var parser : XMLParser = XMLParser(contentsOf: url!)!
        parser.delegate = self
        parser.parse()
        first = false
        parser = XMLParser(contentsOf: url!)!
        parser.delegate = self
        parser.parse()
    }
    
    /// There are three attributes; name, start, and end. If a node is in a startState it is tagged as 'yes', otherwise 'no'.
    /// Also, if a node is in a startState, additional attribute will be fetched; originalPos that represents its original
    /// part of speech.
    /// - Parameters:
    ///   - parser: Current parser
    ///   - elementName: Name of the element
    ///   - namespaceURI: -
    ///   - qName: -
    ///   - attributeDict: Attribute list of the element
    public func parser(_ parser: XMLParser, didStartElement elementName: String, namespaceURI: String?, qualifiedName qName: String?, attributes attributeDict: [String : String]) {
        var name, originalpos: String
        var start, end: Bool
        if elementName == "state" {
            if first{
                name = attributeDict["name"]!
                start = attributeDict["start"]! == "yes"
                end = attributeDict["end"]! == "yes"
                if start{
                    originalpos = attributeDict["originalpos"]!
                    state = FsmState(name: name, startState: true, endState: end, pos: originalpos)
                } else {
                    state = FsmState(name: name, startState: false, endState: end)
                }
            } else {
                name = attributeDict["name"]!
                for state1 in states{
                    if state1.getName() == name{
                        state = state1
                        break
                    }
                }
            }
        } else {
            if elementName == "to"{
                if !first{
                    toState = getState(name: attributeDict["name"]!)!
                    if attributeDict["transitionname"] != nil{
                        withName = attributeDict["transitionname"]
                    } else {
                        withName = nil
                    }
                    if attributeDict["topos"] != nil{
                        rootToPos = attributeDict["topos"]
                    } else {
                        rootToPos = nil
                    }
                }
            } else {
                if elementName == "with"{
                    if !first{
                        value = ""
                        if attributeDict["name"] != nil{
                            withName = attributeDict["name"]
                        }
                        if attributeDict["topos"] != nil{
                            toPos = attributeDict["topos"]
                        } else {
                            toPos = nil
                        }
                    }
                }
            }
        }
    }
    
    /// It gets states by the tag name 'state' and puts them into an array called states.
    /// - Parameters:
    ///   - parser: Current parser
    ///   - elementName: Name of the element
    ///   - namespaceURI: -
    ///   - qName: -
    public func parser(_ parser: XMLParser, didEndElement elementName: String, namespaceURI: String?, qualifiedName qName: String?){
        if elementName == "state" && first{
            states.append(state!)
            value = ""
        } else {
            if elementName == "with"{
                if !first{
                    if toPos == nil{
                        if rootToPos == nil{
                            addTransition(fromState: state!, toState: toState!, with: value, withName: withName)
                        } else {
                            addTransition(fromState: state!, toState: toState!, with: value, withName: withName, toPos: rootToPos!)
                        }
                    } else {
                        addTransition(fromState: state!, toState: toState!, with: value, withName: withName!, toPos: toPos!)
                    }
                    value = ""
                }
            }
        }
    }
    
    /// -
    /// - Parameters:
    ///   - parser: Current parser
    ///   - string: Text to be processed.
    public func parser(_ parser: XMLParser, foundCharacters string: String){
        if string != "\n"{
            value = value + string
        }
    }

    /**
     * The isValidTransition loops through states ArrayList and checks transitions between states. If the actual transition
     * equals to the given transition input, method returns true otherwise returns false.
        - Parameters:
            - transition: is used to compare with the actual transition of a state.
        - Returns: true when the actual transition equals to the transition input, false otherwise.
     */
    public func isValidTransition(transition: String) -> Bool{
        for state in transitions.keys {
            let transitionList : [Transition] = transitions[state]!
            for transition1 in transitionList {
                if transition1.description() == transition {
                    return true
                }
            }
        }
        return false
    }
    
    /**
     * the getStates method returns the states in the FiniteStateMachine.
        - Returns: StateList.
     */
    public func getStates() -> [FsmState]{
        return states
    }
    
    /**
     * The getState method is used to loop through the states {@link ArrayList} and return the state whose name equal
     * to the given input name.
        - Parameters:
            - name: is used to compare with the state's actual name.
        - Returns: state if found any, null otherwise.
     */
    public func getState(name: String) -> FsmState?{
        for state in states {
            if state.getName() == name {
                return state
            }
        }
        return nil
    }
    
    /**
     * The addTransition method creates a new {@link Transition} with given input parameters and adds the transition to
     * transitions {@link ArrayList}.
        - Parameters:
            - fromState:  State type input indicating the from state.
            - toState:  State type input indicating the next state.
            - with:     String input indicating with what the transition will be made.
            - withName: String input.
     */
    public func addTransition(fromState: FsmState, toState: FsmState, with: String, withName: String?){
        var transitionList: [Transition] = []
        let newTransition : Transition = Transition(toState: toState, with: with, withName: withName)
        if transitions[fromState] != nil {
            transitionList = transitions[fromState]!
        } else {
            transitionList = []
        }
        transitionList.append(newTransition)
        transitions[fromState] = transitionList
    }
    
    /**
     * Another addTransition method which takes additional argument; toPos and. It creates a new {@link Transition}
     * with given input parameters and adds the transition to transitions {@link ArrayList}.
        - Parameters:
            - fromState:  State type input indicating the from state.
            - toState:  State type input indicating the next state.
            - with:     String input indicating with what the transition will be made.
            - withName: String input.
            - toPos:    String input.
     */
    public func addTransition(fromState: FsmState, toState: FsmState, with: String, withName: String?, toPos: String){
        var transitionList: [Transition] = []
        let newTransition : Transition = Transition(toState: toState, with: with, withName: withName, toPos: toPos)
        if transitions[fromState] != nil {
            transitionList = transitions[fromState]!
        } else {
            transitionList = []
        }
        transitionList.append(newTransition)
        transitions[fromState] = transitionList
    }
    
    /**
     * The getTransitions method returns the transitions at the given state.
        - Parameters:
            - state: State input.
        - Returns: transitions at given state.
     */
    public func getTransitions(state: FsmState) -> [Transition]{
        if transitions[state] != nil{
            return transitions[state]!
        } else {
            return []
        }
    }
}

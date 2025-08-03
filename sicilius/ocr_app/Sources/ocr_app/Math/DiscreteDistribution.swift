//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 16.08.2020.
//

import Foundation

public class DiscreteDistribution{
    
    private var sum: Double = 0.0
    private var data: [String: Int] = [:]
    private var keys: [String] = []

    public init(){
    }
    
    /**
    The addItem method takes a String item as an input and if this map contains a mapping for the item it puts the
    item with given value + 1, else it puts item with value of 1.

    PARAMETERS
    ----------
    item : Stringing
        String input.
    */
    public func addItem(item: String){
        if data[item] != nil{
            data[item] = data[item]! + 1
        } else {
            keys.append(item)
            data[item] = 1
        }
        self.sum = self.sum + 1
    }

    /**
    The removeItem method takes a String item as an input and if this map contains a mapping for the item it puts
    the item with given value - 1, and if its value is 0, it removes the item.

    - Parameter item : String input.
    */
    public func removeItem(item: String){
        if data[item] != nil{
            data[item] = data[item]! - 1
            if data[item] == 0{
                data[item] = nil
                keys.remove(at: keys.firstIndex(of: item)!)
            }
            self.sum = self.sum - 1
        }
    }

    /**
    The addDistribution method takes a DiscreteDistribution as an input and loops through the entries in this
    distribution and if this map contains a mapping for the entry it puts the entry with its value + entry,
    else it puts entry with its value. It also accumulates the values of entries and assigns to the sum variable.

    - Parameter distribution : DiscreteDistribution type input.
    */
    public func addDistribution(distribution: DiscreteDistribution){
        for entry in distribution.data.keys{
            if data[entry] != nil{
                data[entry] = data[entry]! + distribution.data[entry]!
            } else {
                data[entry] = distribution.data[entry]
                keys.append(entry)
            }
            self.sum += Double(distribution.data[entry]!)
        }
    }

    /**
    The removeDistribution method takes a DiscreteDistribution as an input and loops through the entries in this
    distribution and if this map contains a mapping for the entry it puts the entry with its key - value, else it
    removes the entry. It also decrements the value of entry from sum and assigns to the sum variable.

    - Parameter distribution : DiscreteDistribution type input.
    */
    public func removeDistribution(distribution: DiscreteDistribution){
        for entry in distribution.data.keys{
            if data[entry]! - distribution.data[entry]! != 0{
                data[entry]! -= distribution.data[entry]!
            } else {
                data[entry] = nil
                keys.remove(at: keys.firstIndex(of: entry)!)
            }
            self.sum -= Double(distribution.data[entry]!)
        }
    }

    /**
    The getter for sum variable.

    - Returns: sum
    */
    public func getSum() -> Double{
        return self.sum
    }

    /**
    The getIndex method takes an item as an input and returns the index of given item.

    - Parameter item : item to search for index.

    - Returns: index of given item.
    */
    public func getIndex(item: String) -> Int{
        return keys.firstIndex(of: item)!
    }

    /**
    The containsItem method takes an item as an input and returns true if this map contains a mapping for the
    given item.

    - Parameter item : item to check.

    - Returns: true if this map contains a mapping for the given item.
    */
    public func containsItem(item: String) -> Bool{
        return data[item] != nil
    }

    /**
    The getItem method takes an index as an input and returns the item at given index.

    - Parameter index : index is used for searching the item.

    - Returns: the item at given index.
    */
    public func getItem(index: Int) -> String{
        return keys[index]
    }

    /**
    The getValue method takes an index as an input and returns the value at given index.

    - Parameter index : index is used for searching the value.

    - Returns: the value at given index.
    */
    public func getValue(index: Int) -> Int{
        return data[keys[index]]!
    }

    /**
    The getCount method takes an item as an input returns the value to which the specified item is mapped, or ""
    if this map contains no mapping for the key.

    - Parameter item : String

    - Returns: the value to which the specified item is mapped
    */
    public func getCount(item: String) -> Int{
        return data[item]!
    }

    /**
    The getMaxItem method loops through the entries and gets the entry with maximum value.

    - Returns: the entry with maximum value.
    */
    public func getMaxItem() -> String{
        var maxValue : Int = -1
        var maxItem : String = ""
        for item in data.keys{
            if data[item]! > maxValue{
                maxValue = data[item]!
                maxItem = item
            }
        }
        return maxItem
    }
    
    
    /// Returns size of the distribution
    /// - Returns: Size of the distribution
    public func size() -> Int{
        return data.count
    }

    /**
    Another getMaxItem method which takes a list of Strings. It loops through the items in this list
    and gets the item with maximum value.

    - Parameter includeTheseOnly : list of Strings.

    - Returns: the item with maximum value.
    */
    public func getMaxItemIncludeTheseOnly(includeTheseOnly: [String]) -> String{
        var maxValue : Int = -1
        var maxItem : String = ""
        for item in includeTheseOnly{
            var frequency : Int = 0
            if data[item] != nil{
                frequency = data[item]!
            }
            if frequency > maxValue{
                maxValue = frequency
                maxItem = item
            }
        }
        return maxItem
    }

    /**
    The getProbability method takes an item as an input returns the value to which the specified item is mapped over
    sum, or 0.0 if this map contains no mapping for the key.

    - Parameter item : is used to search for probability.

    - Returns: the probability to which the specified item is mapped.
    */
    public func getProbability(item: String) -> Double{
        if data[item] != nil{
            return Double(data[item]!) / self.sum
        } else{
            return 0.0
        }
    }
    
    /// Returns the distribution as a probability distribution
    /// - Returns: Probability distribution
    public func getProbabilityDistribution() -> [String : Double]{
        var result : [String: Double] = [:]
        for item in keys{
            result[item] = getProbability(item: item)
        }
        return result
    }

    /**
    The getProbabilityLaplaceSmoothing method takes an item as an input returns the smoothed value to which the
    specified item is mapped over sum, or 1.0 over sum if this map contains no mapping for the key.
    - Parameter item : is used to search for probability.

    - Returns: the smoothed probability to which the specified item is mapped.
    */
    public func getProbabilityLaplaceSmoothing(item: String) -> Double{
        if data[item] != nil{
            return (Double(data[item]!) + 1.0) / (self.sum + Double(data.count) + 1.0)
        } else {
            return 1.0 / (self.sum + Double(data.count) + 1.0)
        }
    }

    /**
    The entropy method loops through the values and calculates the entropy of these values.

    - Returns: entropy value.
    */
    public func entropy() -> Double{
        var total : Double = 0.0
        for count in data.values{
            let probability : Double = Double(count) / self.sum
            total += -probability * log2(probability)
        }
        return total
    }
    
    /// Returns the item list.
    /// - Returns: Item list.
    public func keySet() -> [String]{
        return keys
    }
}

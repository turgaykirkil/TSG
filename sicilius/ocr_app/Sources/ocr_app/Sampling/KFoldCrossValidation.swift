//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 15.08.2020.
//

import Foundation


public class KFoldCrossValidation<T> : CrossValidation<T>{
    
    private var instanceList: [T]
    private var N: Int

    /**
    A constructor of KFoldCrossValidation class which takes a sample as an array of instances, a K (K in K-fold
    cross-validation) and a seed number, then shuffles the original sample using this seed as random number.

    - Parameters:
        - instanceList : Original sample
        - K : K in K-fold cross-validation
        - seed : Random number to create K-fold sample(s)
    */
    public init(instanceList: [T], K: Int, seed: Int){
        self.instanceList = instanceList
        self.N = instanceList.count
        let random = Random(seed: seed)
        for i in stride(from: instanceList.count - 1, to: 0, by: -1){
            let randomIndex = random.nextInt(maxRange: i + 1)
            let tmp = self.instanceList[i]
            self.instanceList[i] = self.instanceList[randomIndex]
            self.instanceList[randomIndex] = tmp
        }
        super.init()
        self.K = K
    }

    /**
    getTrainFold returns the k'th train fold in K-fold cross-validation.

    - Parameter k : index for the k'th train fold of the K-fold cross-validation

    - Returns: Produced training sample
    */
    public override func getTrainFold(k: Int) -> [T]{
        var trainFold : [T] = []
        for i in 0..<k * self.N / self.K{
            trainFold.append(self.instanceList[i])
        }
        for i in (k + 1) * self.N / self.K..<self.N{
            trainFold.append(self.instanceList[i])
        }
        return trainFold
    }

    /**
    getTestFold returns the k'th test fold in K-fold cross-validation.

    - Parameter k : index for the k'th test fold of the K-fold cross-validation

    - Returns: Produced testing sample
    */
    public override func getTestFold(k: Int) -> [T]{
        var testFold : [T] = []
        for i in k * self.N / self.K..<(k + 1) * self.N / self.K{
            testFold.append(self.instanceList[i])
        }
        return testFold
    }

}

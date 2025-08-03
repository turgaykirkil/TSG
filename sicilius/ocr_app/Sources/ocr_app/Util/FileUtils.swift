//
//  File.swift
//  
//
//  Created by Olcay Taner YILDIZ on 4.04.2021.
//

import Foundation

public class FileUtils{
    
    public static func getLines(fileName: String, fileExtension: String) -> [String]?{
        let thisSourceFile = URL(fileURLWithPath: #file)
        let thisDirectory = thisSourceFile.deletingLastPathComponent()
        let url = thisDirectory.appendingPathComponent(fileName + "." + fileExtension)
        do{
            let fileContent = try String(contentsOf: url, encoding: .utf8)
            return fileContent.split(whereSeparator: \.isNewline).map(String.init)
        } catch {
            return nil
        }
    }

    public static func getItems(fileName: String, fileExtension: String) -> [[String]]?{
        var items : [[String]] = []
        let thisSourceFile = URL(fileURLWithPath: #file)
        let thisDirectory = thisSourceFile.deletingLastPathComponent()
        let url = thisDirectory.appendingPathComponent(fileName + "." + fileExtension)
        do{
            let fileContent = try String(contentsOf: url, encoding: .utf8)
            let lines : [String] = fileContent.split(whereSeparator: \.isNewline).map(String.init)
            for line in lines{
                let wordList : [String] = line.split(separator: " ").map(String.init)
                items.append(wordList)
            }
            return items
        } catch {
            return nil
        }
    }
}

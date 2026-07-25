import Foundation
import Vision
import AppKit
import CoreImage

// Check for input argument
guard CommandLine.arguments.count > 1 else {
    print("Usage: swift vision_ocr.swift <image_path>")
    exit(1)
}

let imagePath = CommandLine.arguments[1]
let imageUrl = URL(fileURLWithPath: imagePath)

guard let image = NSImage(contentsOf: imageUrl),
      let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("Error: Could not load image at \(imagePath)")
    exit(1)
}

let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])

let request = VNRecognizeTextRequest { request, error in
    if let error = error {
        print("Vision Error: \(error.localizedDescription)")
        return
    }
    
    guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
    
    // Sort observations: Group into headers/full-width and two columns (left and right)
    // Page headers (Gazette banner, page number) live strictly at the top margin (y > 0.94 or full width at y > 0.90)
    var headers: [VNRecognizedTextObservation] = []
    var leftColumn: [VNRecognizedTextObservation] = []
    var rightColumn: [VNRecognizedTextObservation] = []
    
    for obs in observations {
        let box = obs.boundingBox
        let y = box.origin.y
        let centerX = box.origin.x + box.size.width / 2.0
        
        if y > 0.94 || (box.size.width > 0.70 && y > 0.90) {
            headers.append(obs)
        } else if centerX < 0.50 {
            leftColumn.append(obs)
        } else {
            rightColumn.append(obs)
        }
    }
    
    // Sort headers: top-to-bottom first, then left-to-right
    headers.sort {
        if abs($0.boundingBox.origin.y - $1.boundingBox.origin.y) > 0.02 {
            return $0.boundingBox.origin.y > $1.boundingBox.origin.y
        }
        return $0.boundingBox.origin.x < $1.boundingBox.origin.x
    }
    
    func groupAndJoin(_ observations: [VNRecognizedTextObservation], lineThreshold: CGFloat) -> String {
        guard !observations.isEmpty else { return "" }
        
        var lines: [[VNRecognizedTextObservation]] = []
        
        for obs in observations {
            let y = obs.boundingBox.origin.y + obs.boundingBox.size.height / 2.0
            
            var added = false
            for i in 0..<lines.count {
                let lineY = lines[i][0].boundingBox.origin.y + lines[i][0].boundingBox.size.height / 2.0
                if abs(y - lineY) <= lineThreshold {
                    lines[i].append(obs)
                    added = true
                    break
                }
            }
            
            if !added {
                lines.append([obs])
            }
        }
        
        // Sort each line by X coordinate (left to right)
        for i in 0..<lines.count {
            lines[i].sort { $0.boundingBox.origin.x < $1.boundingBox.origin.x }
        }
        
        // Sort lines by Y coordinate descending (top to bottom)
        lines.sort {
            let y0 = $0[0].boundingBox.origin.y + $0[0].boundingBox.size.height / 2.0
            let y1 = $1[0].boundingBox.origin.y + $1[0].boundingBox.size.height / 2.0
            return y0 > y1
        }
        
        var textLines: [String] = []
        for line in lines {
            let lineStrings = line.compactMap { $0.topCandidates(1).first?.string }
            textLines.append(lineStrings.joined(separator: " "))
        }
        
        return textLines.joined(separator: "\n")
    }

    let lineThreshold: CGFloat = 0.005
    let headersText = groupAndJoin(headers, lineThreshold: lineThreshold)
    let leftText = groupAndJoin(leftColumn, lineThreshold: lineThreshold)
    let rightText = groupAndJoin(rightColumn, lineThreshold: lineThreshold)
    
    var outputParts: [String] = []
    if !headersText.isEmpty { outputParts.append(headersText) }
    if !leftText.isEmpty { outputParts.append(leftText) }
    if !rightText.isEmpty { outputParts.append(rightText) }
    
    print(outputParts.joined(separator: "\n"))
}

// Optimization for Turkish Trade Registry (TSG) documents
request.recognitionLevel = .accurate
request.recognitionLanguages = ["tr-TR"]
request.usesLanguageCorrection = false

do {
    try requestHandler.perform([request])
} catch {
    print("Failed to perform Vision request: \(error.localizedDescription)")
    exit(1)
}

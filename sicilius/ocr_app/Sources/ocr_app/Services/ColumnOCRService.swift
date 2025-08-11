import Foundation
import Vision
import CoreGraphics

struct ColumnOCRService {
    struct Config {
        var maxColumns: Int = 6
        var bucketCount: Int = 300
        var minColumnWidthFraction: CGFloat = 0.12 // ~1/8 sayfa
        var histogramSmoothWindow: Int = 5
        var gutterThresholdFraction: CGFloat = 0.10 // maxCount * 0.10
        var horizontalMargin: Int = 6
    }

    private let config: Config

    init(config: Config = Config()) {
        self.config = config
    }

    // Ana giriş: sayfayı sütunlara böl ve her sütunu ayrı OCR et
    func recognizePageWithColumns(cgImage: CGImage, languages: [String]) throws -> String {
        // 1) Hızlı modda ön tespit (sadece kutular)
        let observations = try recognizeBoxesFast(cgImage: cgImage, languages: languages)
        // 2) Histogram tabanlı sütun aralıklarını bul
        let xRanges = detectColumnXRanges(imageWidth: cgImage.width, observations: observations)
        // 3) Fallback: sütun bulunamadıysa tüm sayfayı tek sütun kabul et
        if xRanges.count <= 1 {
            return try recognizeAccurate(cgImage: cgImage, languages: languages)
        }
        // 4) Her sütunu kırpıp .accurate ile OCR et
        var parts: [String] = []
        for r in xRanges {
            let x0 = max(0, r.lowerBound - config.horizontalMargin)
            let x1 = min(cgImage.width, r.upperBound + config.horizontalMargin)
            let w = max(1, x1 - x0)
            let rect = CGRect(x: x0, y: 0, width: w, height: cgImage.height)
            if let crop = cgImage.cropping(to: rect) {
                let txt = try recognizeAccurate(cgImage: crop, languages: languages)
                if !txt.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                    parts.append(txt)
                }
            }
        }
        return parts.joined(separator: "\n")
    }

    // Vision hızlı modda kutular
    private func recognizeBoxesFast(cgImage: CGImage, languages: [String]) throws -> [VNRecognizedTextObservation] {
        let request = VNRecognizeTextRequest()
        request.recognitionLevel = .fast
        request.usesLanguageCorrection = false
        request.recognitionLanguages = languages
        let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
        try handler.perform([request])
        return request.results ?? []
    }

    // Doğru modda metin al
    private func recognizeAccurate(cgImage: CGImage, languages: [String]) throws -> String {
        let request = VNRecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.usesLanguageCorrection = true
        request.recognitionLanguages = languages
        let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
        try handler.perform([request])
        let observations = request.results ?? []
        let text = observations.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
        return text
    }

    // Dikey histogram ile sütun aralıklarını tespit
    private func detectColumnXRanges(imageWidth: Int, observations: [VNRecognizedTextObservation]) -> [ClosedRange<Int>] {
        guard imageWidth > 0, !observations.isEmpty else { return [] }
        let bucketCount = max(60, min(config.bucketCount, imageWidth))
        var buckets = Array(repeating: 0, count: bucketCount)

        // Observation bbox'ları normalized [0,1]. Y eksenini dikkate almadan sadece x aralığını işliyoruz.
        func xToBucket(_ x: CGFloat) -> Int {
            let clamped = max(0, min(1, x))
            return Int((CGFloat(bucketCount) * clamped).rounded(.down))
        }

        for obs in observations {
            let bb = obs.boundingBox // normalized (origin bottom-left)
            let x0 = xToBucket(bb.minX)
            let x1 = xToBucket(bb.maxX)
            let lo = max(0, min(bucketCount - 1, min(x0, x1)))
            let hi = max(0, min(bucketCount - 1, max(x0, x1)))
            if hi >= lo {
                for i in lo...hi { buckets[i] &+= 1 }
            }
        }

        // Yumuşatma (moving average)
        let win = max(1, config.histogramSmoothWindow)
        if win > 1 {
            var smoothed = Array(repeating: 0, count: bucketCount)
            var acc = 0
            for i in 0..<bucketCount {
                acc += buckets[i]
                if i >= win { acc -= buckets[i - win] }
                smoothed[i] = acc / min(win, i + 1)
            }
            buckets = smoothed
        }

        guard let maxVal = buckets.max(), maxVal > 0 else { return [] }
        let threshold = max(1, Int(CGFloat(maxVal) * config.gutterThresholdFraction))

        // Gutters = düşük yoğunluklu kesitler
        var gutters: [ClosedRange<Int>] = []
        var i = 0
        while i < bucketCount {
            if buckets[i] <= threshold {
                let start = i
                while i < bucketCount && buckets[i] <= threshold { i += 1 }
                let end = i - 1
                gutters.append(start...end)
            } else {
                i += 1
            }
        }

        // Sütunlar = gutters arasındaki aralıklar
        var columns: [ClosedRange<Int>] = []
        var prevEnd = -1
        for g in gutters {
            let colStart = prevEnd + 1
            let colEnd = g.lowerBound - 1
            if colEnd >= colStart { columns.append(colStart...colEnd) }
            prevEnd = g.upperBound
        }
        if prevEnd < bucketCount - 1 {
            columns.append((prevEnd + 1)...(bucketCount - 1))
        }

        // Piksel aralıklarına çevir ve filtrele
        func bucketToX(_ b: Int) -> Int {
            return Int((Double(b) / Double(bucketCount)) * Double(imageWidth))
        }
        var pixelColumns: [ClosedRange<Int>] = columns.map { b in
            let x0 = max(0, min(imageWidth - 1, bucketToX(b.lowerBound)))
            let x1 = max(0, min(imageWidth, bucketToX(b.upperBound + 1)))
            return x0...(max(x0 + 1, x1))
        }

        let minWidthPx = max(32, Int(CGFloat(imageWidth) * config.minColumnWidthFraction))
        pixelColumns = pixelColumns.filter { ($0.upperBound - $0.lowerBound) >= minWidthPx }

        // Çok fazla sütun varsa komşu dar sütunları birleştir
        while pixelColumns.count > config.maxColumns {
            // En dar aralığı bul ve komşusuyla birleştir
            var minIdx = 0
            var minWidth = Int.max
            for (idx, r) in pixelColumns.enumerated() {
                let w = r.upperBound - r.lowerBound
                if w < minWidth { minWidth = w; minIdx = idx }
            }
            if minIdx > 0 {
                let merged = pixelColumns[minIdx - 1].lowerBound...max(pixelColumns[minIdx - 1].upperBound, pixelColumns[minIdx].upperBound)
                pixelColumns[minIdx - 1] = merged
                pixelColumns.remove(at: minIdx)
            } else if pixelColumns.count >= 2 {
                let merged = pixelColumns[0].lowerBound...max(pixelColumns[0].upperBound, pixelColumns[1].upperBound)
                pixelColumns[0] = merged
                pixelColumns.remove(at: 1)
            } else {
                break
            }
        }

        // Soldan sağa sırala
        pixelColumns.sort { $0.lowerBound < $1.lowerBound }
        return pixelColumns
    }
}

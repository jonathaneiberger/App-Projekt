import Foundation

enum BotEngine {
    static func chooseIndex(from options: [Int], difficulty: BotDifficulty) -> Int? {
        guard !options.isEmpty else { return nil }

        let skillChance = difficulty.reactionFactor
        if Double.random(in: 0...1) <= skillChance {
            return options.randomElement()
        }

        return options.shuffled().first
    }

    static func hitChance(for difficulty: BotDifficulty) -> Double {
        switch difficulty {
        case .easy: return 0.30
        case .medium: return 0.50
        case .hard: return 0.72
        case .veryHard: return 0.88
        }
    }
}

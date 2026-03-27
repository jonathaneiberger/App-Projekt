import Foundation

enum BotDifficulty: String, CaseIterable, Identifiable {
    case easy = "Leicht"
    case medium = "Mittel"
    case hard = "Schwer"
    case veryHard = "Sehr schwer"

    var id: String { rawValue }

    var reactionFactor: Double {
        switch self {
        case .easy: return 0.35
        case .medium: return 0.55
        case .hard: return 0.75
        case .veryHard: return 0.9
        }
    }
}

struct ArcadeGame: Identifiable {
    let id = UUID()
    let title: String
    let description: String
    let supportsBot: Bool
    let supportsMultiplayer: Bool
}

let defaultGames: [ArcadeGame] = [
    .init(title: "Fußball-Duell", description: "Penalty-Shooter gegen Bot", supportsBot: true, supportsMultiplayer: false),
    .init(title: "Tischtennis", description: "Reflexspiel im Pong-Stil", supportsBot: true, supportsMultiplayer: true),
    .init(title: "Schiffe versenken", description: "Grid-Taktik gegen Bot", supportsBot: true, supportsMultiplayer: false),
    .init(title: "TicTacToe", description: "3x3 mit Bot oder lokal 2P", supportsBot: true, supportsMultiplayer: true),
    .init(title: "Rennspiel", description: "Lane Runner mit Hindernissen", supportsBot: false, supportsMultiplayer: false),
    .init(title: "Tank Battle", description: "Tank zerstört Tank", supportsBot: true, supportsMultiplayer: true),
    .init(title: "Parkour Dash", description: "Jump-n-Run im Side-Runner-Stil", supportsBot: false, supportsMultiplayer: false),
    .init(title: "Memory", description: "Karten-Paare finden", supportsBot: false, supportsMultiplayer: true),
    .init(title: "Code-Knacker", description: "Rate den Geheimcode", supportsBot: false, supportsMultiplayer: false)
]

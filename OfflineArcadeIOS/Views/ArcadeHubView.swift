import SwiftUI

struct ArcadeHubView: View {
    @State private var selectedDifficulty: BotDifficulty = .medium

    var body: some View {
        NavigationStack {
            List {
                Section("Bot-Schwierigkeit") {
                    Picker("Schwierigkeit", selection: $selectedDifficulty) {
                        ForEach(BotDifficulty.allCases) { level in
                            Text(level.rawValue).tag(level)
                        }
                    }
                    .pickerStyle(.segmented)
                }

                Section("Spiele") {
                    NavigationLink("Fußball-Duell") { SoccerDuelView(difficulty: selectedDifficulty) }
                    NavigationLink("Tischtennis") { TableTennisView(difficulty: selectedDifficulty) }
                    NavigationLink("Schiffe versenken") { BattleshipView(difficulty: selectedDifficulty) }
                    NavigationLink("TicTacToe") { TicTacToeView(difficulty: selectedDifficulty) }
                    NavigationLink("Rennspiel") { RacingView() }
                    NavigationLink("Tank Battle") { TankBattleView(difficulty: selectedDifficulty) }
                    NavigationLink("Parkour Dash") { ParkourView() }
                    NavigationLink("Memory") { MemoryView() }
                    NavigationLink("Code-Knacker") { CodeBreakerView() }
                }
            }
            .navigationTitle("Offline Arcade")
        }
    }
}

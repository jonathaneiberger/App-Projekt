import SwiftUI

struct TableTennisView: View {
    @StateObject private var mp = LocalMultiplayerService()
    @State private var player = 0
    @State private var bot = 0

    let difficulty: BotDifficulty

    var body: some View {
        VStack(spacing: 12) {
            Text("Tischtennis")
                .font(.title2.bold())
            Text("Du \(player) : \(bot) Bot")
            Text("Tippe schnell auf Return")

            Button("🏓 Return") {
                rally()
            }
            .buttonStyle(.borderedProminent)

            Toggle("Lokaler Multiplayer-Modus", isOn: Binding(
                get: { mp.isSessionActive },
                set: { $0 ? mp.startLocalSession() : mp.stopLocalSession() }
            ))
            Text(mp.statusText).font(.footnote).foregroundStyle(.secondary)

            Button("Reset") { player = 0; bot = 0 }
        }
        .padding()
    }

    private func rally() {
        if Double.random(in: 0...1) > BotEngine.hitChance(for: difficulty) {
            player += 1
        } else {
            bot += 1
        }
    }
}

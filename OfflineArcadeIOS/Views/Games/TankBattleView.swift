import SwiftUI

struct TankBattleView: View {
    @StateObject private var mp = LocalMultiplayerService()
    @State private var playerHP = 100
    @State private var botHP = 100
    @State private var status = "Bereit"

    let difficulty: BotDifficulty

    var body: some View {
        VStack(spacing: 12) {
            Text("Tank Battle")
                .font(.title2.bold())
            Text("Du: \(playerHP) HP | Gegner: \(botHP) HP")
            Text(status)

            HStack {
                Button("Standard-Schuss") { attack(multiplier: 1.0) }
                Button("Rakete") { attack(multiplier: 1.6) }
            }
            .buttonStyle(.borderedProminent)

            Toggle("Lokaler Multiplayer-Modus", isOn: Binding(
                get: { mp.isSessionActive },
                set: { $0 ? mp.startLocalSession() : mp.stopLocalSession() }
            ))
            Text(mp.statusText).font(.footnote).foregroundStyle(.secondary)

            Button("Neue Schlacht") { reset() }
        }
        .padding()
    }

    private func attack(multiplier: Double) {
        guard playerHP > 0 && botHP > 0 else { return }

        let playerDamage = Int(Double(Int.random(in: 10...20)) * multiplier)
        botHP = max(0, botHP - playerDamage)

        if botHP == 0 {
            status = "Du hast gewonnen!"
            return
        }

        let botBase = Int.random(in: 8...22)
        let botDamage = Int(Double(botBase) * difficulty.reactionFactor)
        playerHP = max(0, playerHP - botDamage)

        status = playerHP == 0 ? "Du wurdest zerstört" : "Du triffst für \(playerDamage), Bot für \(botDamage)"
    }

    private func reset() {
        playerHP = 100
        botHP = 100
        status = "Bereit"
    }
}

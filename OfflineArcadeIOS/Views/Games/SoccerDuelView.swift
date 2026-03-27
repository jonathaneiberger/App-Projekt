import SwiftUI

struct SoccerDuelView: View {
    @State private var score = 0
    @State private var rounds = 0
    @State private var result = "Wähle links, mitte oder rechts"

    let difficulty: BotDifficulty

    var body: some View {
        VStack(spacing: 14) {
            Text("Fußball-Duell")
                .font(.title.bold())
            Text("Tore: \(score)/\(rounds)")
            Text(result)
                .multilineTextAlignment(.center)

            HStack {
                shotButton("⬅️", lane: 0)
                shotButton("⬆️", lane: 1)
                shotButton("➡️", lane: 2)
            }

            Button("Neu starten") {
                score = 0; rounds = 0
                result = "Wähle links, mitte oder rechts"
            }
        }
        .padding()
    }

    private func shotButton(_ icon: String, lane: Int) -> some View {
        Button(icon) { shoot(playerLane: lane) }
            .font(.largeTitle)
            .buttonStyle(.borderedProminent)
    }

    private func shoot(playerLane: Int) {
        rounds += 1
        let goalieLane: Int
        if Double.random(in: 0...1) < difficulty.reactionFactor {
            goalieLane = playerLane
        } else {
            goalieLane = Int.random(in: 0...2)
        }

        if goalieLane == playerLane {
            result = "Gehalten vom Keeper!"
        } else {
            score += 1
            result = "TOOOOR!"
        }
    }
}

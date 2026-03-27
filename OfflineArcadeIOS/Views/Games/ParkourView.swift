import SwiftUI

struct ParkourView: View {
    @State private var energy = 100
    @State private var coins = 0
    @State private var obstaclesCleared = 0
    @State private var bag: [String] = []

    var body: some View {
        VStack(spacing: 12) {
            Text("Parkour Dash")
                .font(.title2.bold())
            Text("Energie: \(energy) | Coins: \(coins) | Hindernisse: \(obstaclesCleared)")

            HStack {
                Button("Springen") { jump() }
                Button("Sliden") { slide() }
                Button("Item nutzen") { useItem() }
            }
            .buttonStyle(.borderedProminent)

            Text("Items: \(bag.joined(separator: ", "))")
                .font(.footnote)
                .foregroundStyle(.secondary)

            Button("Neuer Run") { reset() }
        }
        .padding()
    }

    private func jump() {
        encounter(successBias: 0.70)
    }

    private func slide() {
        encounter(successBias: 0.60)
    }

    private func useItem() {
        guard let item = bag.first else { return }
        bag.removeFirst()
        if item == "Medkit" { energy = min(100, energy + 20) }
        if item == "Coin-Magnet" { coins += 10 }
    }

    private func encounter(successBias: Double) {
        if Double.random(in: 0...1) < successBias {
            obstaclesCleared += 1
            coins += Int.random(in: 1...4)
            if Int.random(in: 0...100) > 80 {
                bag.append(Bool.random() ? "Medkit" : "Coin-Magnet")
            }
        } else {
            energy = max(0, energy - Int.random(in: 10...24))
        }
    }

    private func reset() {
        energy = 100
        coins = 0
        obstaclesCleared = 0
        bag.removeAll()
    }
}

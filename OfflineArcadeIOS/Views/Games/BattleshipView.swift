import SwiftUI

struct BattleshipView: View {
    @State private var enemyShips = Set([2, 7, 13, 20, 28])
    @State private var shots = Set<Int>()
    @State private var hits = 0

    let difficulty: BotDifficulty

    var body: some View {
        VStack(spacing: 12) {
            Text("Schiffe versenken")
                .font(.title2.bold())
            Text("Treffer: \(hits)/5 • Bot: \(difficulty.rawValue)")

            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 6), spacing: 4) {
                ForEach(0..<36, id: \.self) { idx in
                    Button {
                        fire(at: idx)
                    } label: {
                        RoundedRectangle(cornerRadius: 6)
                            .fill(color(for: idx))
                            .frame(height: 38)
                    }
                    .disabled(shots.contains(idx) || hits == 5)
                }
            }

            if hits == 5 {
                Text("Alle Schiffe zerstört!")
                    .foregroundStyle(.green)
            }

            Button("Neue Runde") { reset() }
        }
        .padding()
    }

    private func fire(at idx: Int) {
        shots.insert(idx)
        if enemyShips.contains(idx) { hits += 1 }
    }

    private func color(for idx: Int) -> Color {
        guard shots.contains(idx) else { return .blue.opacity(0.3) }
        return enemyShips.contains(idx) ? .red : .gray
    }

    private func reset() {
        enemyShips = Set((0..<36).shuffled().prefix(5))
        shots.removeAll()
        hits = 0
    }
}

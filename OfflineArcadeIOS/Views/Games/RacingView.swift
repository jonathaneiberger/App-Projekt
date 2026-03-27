import SwiftUI

struct RacingView: View {
    @State private var lane = 1
    @State private var obstacle = Int.random(in: 0...2)
    @State private var distance = 0
    @State private var crashed = false

    var body: some View {
        VStack(spacing: 12) {
            Text("Rennspiel")
                .font(.title2.bold())
            Text("Distanz: \(distance)m")

            Text(crashed ? "💥 Crash!" : "Fahre weiter")
                .foregroundStyle(crashed ? .red : .green)

            HStack {
                ForEach(0..<3, id: \.self) { idx in
                    VStack {
                        Text(lane == idx ? "🚗" : "▫️")
                        Text(obstacle == idx ? "🧱" : " ")
                    }
                    .frame(maxWidth: .infinity)
                }
            }
            .padding()
            .background(.black.opacity(0.06))
            .clipShape(RoundedRectangle(cornerRadius: 12))

            HStack {
                Button("⬅️") { lane = max(0, lane - 1) }
                Button("➡️") { lane = min(2, lane + 1) }
                Button("Gas") { tick() }
            }
            .buttonStyle(.borderedProminent)

            Button("Neue Fahrt") { reset() }
        }
        .padding()
    }

    private func tick() {
        guard !crashed else { return }
        distance += 25
        if lane == obstacle {
            crashed = true
        }
        obstacle = Int.random(in: 0...2)
    }

    private func reset() {
        lane = 1
        obstacle = Int.random(in: 0...2)
        distance = 0
        crashed = false
    }
}

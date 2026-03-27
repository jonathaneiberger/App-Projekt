import SwiftUI

struct CodeBreakerView: View {
    @State private var secret = Int.random(in: 100...999)
    @State private var input = ""
    @State private var hints: [String] = []

    var body: some View {
        VStack(spacing: 12) {
            Text("Code-Knacker")
                .font(.title2.bold())
            Text("Rate den 3-stelligen Code")

            TextField("z.B. 527", text: $input)
                .keyboardType(.numberPad)
                .textFieldStyle(.roundedBorder)

            Button("Prüfen") {
                guess()
            }
            .buttonStyle(.borderedProminent)

            List(hints.reversed(), id: \.self) { row in
                Text(row)
            }
            .frame(height: 180)

            Button("Neues Spiel") { reset() }
        }
        .padding()
    }

    private func guess() {
        guard let value = Int(input), (100...999).contains(value) else {
            hints.append("Ungültige Eingabe")
            input = ""
            return
        }
        if value == secret {
            hints.append("✅ Treffer! Der Code war \(secret)")
        } else if value < secret {
            hints.append("⬆️ Höher als \(value)")
        } else {
            hints.append("⬇️ Niedriger als \(value)")
        }
        input = ""
    }

    private func reset() {
        secret = Int.random(in: 100...999)
        input = ""
        hints.removeAll()
    }
}

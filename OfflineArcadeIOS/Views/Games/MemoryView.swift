import SwiftUI

struct MemoryView: View {
    private let symbols = ["🐶","🐱","🦊","🐼","🐸","🐵"]
    @State private var cards: [String] = []
    @State private var revealed: [Int] = []
    @State private var matched: Set<Int> = []

    var body: some View {
        VStack {
            Text("Memory")
                .font(.title2.bold())

            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 4), spacing: 8) {
                ForEach(cards.indices, id: \.self) { idx in
                    Button {
                        flip(idx)
                    } label: {
                        Text(face(for: idx))
                            .frame(height: 55)
                            .frame(maxWidth: .infinity)
                            .background(.orange.opacity(0.2))
                            .clipShape(RoundedRectangle(cornerRadius: 8))
                    }
                    .disabled(matched.contains(idx) || revealed.contains(idx))
                }
            }

            Button("Neu mischen") { setup() }
                .padding(.top, 8)
        }
        .padding()
        .onAppear(perform: setup)
    }

    private func face(for idx: Int) -> String {
        if matched.contains(idx) || revealed.contains(idx) { return cards[idx] }
        return "❓"
    }

    private func setup() {
        cards = (symbols + symbols).shuffled()
        revealed.removeAll()
        matched.removeAll()
    }

    private func flip(_ idx: Int) {
        revealed.append(idx)
        if revealed.count == 2 {
            let a = revealed[0], b = revealed[1]
            if cards[a] == cards[b] {
                matched.insert(a)
                matched.insert(b)
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.6) {
                revealed.removeAll()
            }
        }
    }
}

import SwiftUI

struct TicTacToeView: View {
    @State private var board = Array(repeating: "", count: 9)
    @State private var current = "X"
    @State private var message = "Du bist X"

    let difficulty: BotDifficulty

    var body: some View {
        VStack(spacing: 12) {
            Text("TicTacToe")
                .font(.title.bold())
            Text(message)

            LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 3), spacing: 8) {
                ForEach(0..<9, id: \.self) { idx in
                    Button(board[idx].isEmpty ? " " : board[idx]) {
                        makeMove(idx)
                    }
                    .frame(width: 70, height: 70)
                    .background(.blue.opacity(0.15))
                    .font(.title2.bold())
                    .disabled(!board[idx].isEmpty || winner() != nil)
                }
            }

            Button("Neu starten") { reset() }
                .buttonStyle(.borderedProminent)
        }
        .padding()
    }

    private func makeMove(_ idx: Int) {
        guard board[idx].isEmpty else { return }
        board[idx] = "X"

        if let w = winner() {
            message = "Gewinner: \(w)"
            return
        }

        let free = board.indices.filter { board[$0].isEmpty }
        if let botIdx = BotEngine.chooseIndex(from: free, difficulty: difficulty) {
            board[botIdx] = "O"
        }

        if let w = winner() {
            message = "Gewinner: \(w)"
        } else if !board.contains("") {
            message = "Unentschieden"
        }
    }

    private func winner() -> String? {
        let lines = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]

        for line in lines {
            let a = board[line[0]], b = board[line[1]], c = board[line[2]]
            if !a.isEmpty && a == b && b == c { return a }
        }
        return nil
    }

    private func reset() {
        board = Array(repeating: "", count: 9)
        message = "Du bist X"
    }
}

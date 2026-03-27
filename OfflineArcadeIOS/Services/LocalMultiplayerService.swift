import Foundation

final class LocalMultiplayerService: ObservableObject {
    @Published var isSessionActive = false
    @Published var statusText = "Kein Multiplayer aktiv"

    func startLocalSession() {
        isSessionActive = true
        statusText = "Lokaler Multiplayer vorbereitet (MVP-Stub)"
    }

    func stopLocalSession() {
        isSessionActive = false
        statusText = "Multiplayer beendet"
    }
}

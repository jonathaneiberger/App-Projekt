import Foundation
import LocalAuthentication

final class Gatekeeper: ObservableObject {
    @Published var isUnlocked = false
    @Published var errorMessage: String?

    private let fallbackPin = "2907"

    func unlockWithBiometrics() {
        let context = LAContext()
        var error: NSError?

        guard context.canEvaluatePolicy(.deviceOwnerAuthentication, error: &error) else {
            errorMessage = "Biometrie nicht verfügbar. PIN verwenden."
            return
        }

        let reason = "Offline Arcade entsperren"
        context.evaluatePolicy(.deviceOwnerAuthentication, localizedReason: reason) { [weak self] success, evalError in
            DispatchQueue.main.async {
                if success {
                    self?.isUnlocked = true
                } else {
                    self?.errorMessage = evalError?.localizedDescription ?? "Authentifizierung fehlgeschlagen"
                }
            }
        }
    }

    func unlockWithPin(_ pin: String) {
        if pin == fallbackPin {
            isUnlocked = true
            errorMessage = nil
        } else {
            errorMessage = "Falsche PIN"
        }
    }
}

import SwiftUI

struct LockScreenView: View {
    @EnvironmentObject private var gatekeeper: Gatekeeper
    @State private var pin = ""

    var body: some View {
        VStack(spacing: 16) {
            Text("🔒 Offline Arcade")
                .font(.largeTitle.bold())

            Text("Nur berechtigte Nutzer")
                .font(.headline)
                .foregroundStyle(.secondary)

            Button("Mit Face ID / Touch ID entsperren") {
                gatekeeper.unlockWithBiometrics()
            }
            .buttonStyle(.borderedProminent)

            SecureField("PIN eingeben", text: $pin)
                .textFieldStyle(.roundedBorder)
                .frame(maxWidth: 220)

            Button("Mit PIN entsperren") {
                gatekeeper.unlockWithPin(pin)
                pin = ""
            }
            .buttonStyle(.bordered)

            if let error = gatekeeper.errorMessage {
                Text(error)
                    .foregroundStyle(.red)
                    .multilineTextAlignment(.center)
            }
        }
        .padding()
    }
}

import SwiftUI

@main
struct OfflineArcadeApp: App {
    @StateObject private var gatekeeper = Gatekeeper()

    var body: some Scene {
        WindowGroup {
            Group {
                if gatekeeper.isUnlocked {
                    ArcadeHubView()
                } else {
                    LockScreenView()
                }
            }
            .environmentObject(gatekeeper)
        }
    }
}

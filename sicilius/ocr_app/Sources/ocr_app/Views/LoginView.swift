import SwiftUI

struct LoginView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    @State private var email = ""
    @State private var password = ""

    // 1. Odaklanılabilir alanları temsil eden bir enum tanımlayın
    private enum Field: Hashable {
        case email
        case password
    }

    // 2. Hangi alanın odakta olduğunu izlemek için @FocusState kullanın
    @FocusState private var focusedField: Field?

    var body: some View {
        VStack(spacing: 20) {
            Spacer()
            
            Text("Sicilius OCR")
                .font(.largeTitle)
                .fontWeight(.bold)

            Text("Lütfen yönetici hesabınızla giriş yapın.")
                .font(.headline)
                .foregroundColor(.secondary)

            VStack(spacing: 15) {
                TextField("E-posta Adresi", text: $email)
                    .padding(10)
                    .background(Color(.textBackgroundColor))
                    .cornerRadius(8)
                    // 3. Bu alanı odak durumuna bağlayın
                    .focused($focusedField, equals: .email)
                    // 4. Enter'a basıldığında bir sonraki alana geçin
                    .onSubmit {
                        focusedField = .password
                    }
                
                SecureField("Parola", text: $password)
                    .padding(10)
                    .background(Color(.textBackgroundColor))
                    .cornerRadius(8)
                    // 3. Bu alanı odak durumuna bağlayın
                    .focused($focusedField, equals: .password)
                    // 4. Enter'a basıldığında giriş yapmayı deneyin
                    .onSubmit {
                        authViewModel.signIn(email: email, password: password)
                    }
            }
            .padding(.horizontal, 40)

            if authViewModel.isLoading {
                ProgressView()
            } else {
                Button(action: {
                    authViewModel.signIn(email: email, password: password)
                }) {
                    Text("Giriş Yap")
                        .fontWeight(.semibold)
                        .frame(maxWidth: .infinity)
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.large)
                .padding(.horizontal, 40)
            }

            if let errorMessage = authViewModel.errorMessage {
                Text(errorMessage)
                    .foregroundColor(.red)
                    .font(.caption)
                    .padding(.top)
            }
            
            Spacer()
        }
        .frame(width: 400, height: 400)
        // 5. Görünüm ilk açıldığında e-posta alanına odaklanın
        .onAppear {
            // Görünüm ilk açıldığında e-posta alanına odaklanın
            focusedField = .email
        }
    }
}

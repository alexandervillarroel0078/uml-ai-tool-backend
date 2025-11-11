import 'package:flutter/material.dart';
import '../services/api_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  bool loading = false;
  String? errorMessage;

  Future<void> _login() async {
    setState(() {
      loading = true;
      errorMessage = null;
    });

    try {
      final response = await ApiService().postData(
        "auth/login", // 👈 SIN "api/" porque tu backend usa @RequestMapping("/auth")
        {
          "email": emailController.text,
          "password": passwordController.text,
        },
      );

      if (response != null && response["token"] != null) {
        Navigator.pushReplacementNamed(context, '/home'); // ✅ redirige al home
      } else {
        setState(() {
          errorMessage = "Credenciales incorrectas";
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = "Error al conectar con el servidor";
      });
    }

    setState(() {
      loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("🔐 Iniciar Sesión")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: emailController,
              decoration: const InputDecoration(labelText: "Correo"),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: passwordController,
              decoration: const InputDecoration(labelText: "Contraseña"),
              obscureText: true,
            ),
            const SizedBox(height: 20),
            if (errorMessage != null)
              Text(errorMessage!,
                  style: const TextStyle(color: Colors.red, fontSize: 14)),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: loading ? null : _login,
              style: ElevatedButton.styleFrom(
                minimumSize: const Size.fromHeight(50),
              ),
              child: loading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text("Ingresar"),
            ),
          ],
        ),
      ),
    );
  }
}
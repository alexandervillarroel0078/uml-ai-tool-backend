
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class UsuarioDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? usuario;
  const UsuarioDetailScreen({super.key, this.usuario});

  @override
  State<UsuarioDetailScreen> createState() => _UsuarioDetailScreenState();
}

class _UsuarioDetailScreenState extends State<UsuarioDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController nombreController = TextEditingController();
  
  final TextEditingController emailController = TextEditingController();
  
  final TextEditingController passwordController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.usuario != null) {
      
      nombreController.text = widget.usuario!['nombre']?.toString() ?? '';
      
      emailController.text = widget.usuario!['email']?.toString() ?? '';
      
      passwordController.text = widget.usuario!['password']?.toString() ?? '';
      
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> saveUsuario() async {
    setState(() => loading = true);

    final data = {
      
      "nombre": nombreController.text,
      
      "email": emailController.text,
      
      "password": passwordController.text,
      
      
    };

    if (widget.usuario == null) {
      await ApiService().postData("api/usuarios", data);
    } else {
      final id = widget.usuario!["id"];
      await ApiService().putData("api/usuarios/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.usuario == null
            ? "Nuevo Usuario"
            : "Editar Usuario"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            
            TextField(
              controller: nombreController,
              decoration: const InputDecoration(
                labelText: "Nombre",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: emailController,
              decoration: const InputDecoration(
                labelText: "Email",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: passwordController,
              decoration: const InputDecoration(
                labelText: "Password",
              ),
            ),
            const SizedBox(height: 12),
            

            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : saveUsuario,
              child: loading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text("Guardar"),
            ),
          ],
        ),
      ),
    );
  }
}
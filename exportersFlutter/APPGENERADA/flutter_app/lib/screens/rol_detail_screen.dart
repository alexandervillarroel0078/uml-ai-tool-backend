
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class RolDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? rol;
  const RolDetailScreen({super.key, this.rol});

  @override
  State<RolDetailScreen> createState() => _RolDetailScreenState();
}

class _RolDetailScreenState extends State<RolDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController nombreController = TextEditingController();
  
  final TextEditingController descripcionController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.rol != null) {
      
      nombreController.text = widget.rol!['nombre']?.toString() ?? '';
      
      descripcionController.text = widget.rol!['descripcion']?.toString() ?? '';
      
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> saveRol() async {
    setState(() => loading = true);

    final data = {
      
      "nombre": nombreController.text,
      
      "descripcion": descripcionController.text,
      
      
    };

    if (widget.rol == null) {
      await ApiService().postData("api/rols", data);
    } else {
      final id = widget.rol!["id"];
      await ApiService().putData("api/rols/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.rol == null
            ? "Nuevo Rol"
            : "Editar Rol"),
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
              controller: descripcionController,
              decoration: const InputDecoration(
                labelText: "Descripcion",
              ),
            ),
            const SizedBox(height: 12),
            

            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : saveRol,
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
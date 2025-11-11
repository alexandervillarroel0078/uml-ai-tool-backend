
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class DepartamentoDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? departamento;
  const DepartamentoDetailScreen({super.key, this.departamento});

  @override
  State<DepartamentoDetailScreen> createState() => _DepartamentoDetailScreenState();
}

class _DepartamentoDetailScreenState extends State<DepartamentoDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController nombreController = TextEditingController();
  
  final TextEditingController ubicacionController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.departamento != null) {
      
      nombreController.text = widget.departamento!['nombre']?.toString() ?? '';
      
      ubicacionController.text = widget.departamento!['ubicacion']?.toString() ?? '';
      
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> saveDepartamento() async {
    setState(() => loading = true);

    final data = {
      
      "nombre": nombreController.text,
      
      "ubicacion": ubicacionController.text,
      
      
    };

    if (widget.departamento == null) {
      await ApiService().postData("api/departamentos", data);
    } else {
      final id = widget.departamento!["id"];
      await ApiService().putData("api/departamentos/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.departamento == null
            ? "Nuevo Departamento"
            : "Editar Departamento"),
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
              controller: ubicacionController,
              decoration: const InputDecoration(
                labelText: "Ubicacion",
              ),
            ),
            const SizedBox(height: 12),
            

            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : saveDepartamento,
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
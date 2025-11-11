
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class CursoDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? curso;
  const CursoDetailScreen({super.key, this.curso});

  @override
  State<CursoDetailScreen> createState() => _CursoDetailScreenState();
}

class _CursoDetailScreenState extends State<CursoDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController nombreController = TextEditingController();
  
  final TextEditingController nivelController = TextEditingController();
  
  final TextEditingController duracionController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.curso != null) {
      
      nombreController.text = widget.curso!['nombre']?.toString() ?? '';
      
      nivelController.text = widget.curso!['nivel']?.toString() ?? '';
      
      duracionController.text = widget.curso!['duracion']?.toString() ?? '';
      
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> saveCurso() async {
    setState(() => loading = true);

    final data = {
      
      "nombre": nombreController.text,
      
      "nivel": nivelController.text,
      
      "duracion": duracionController.text,
      
      
    };

    if (widget.curso == null) {
      await ApiService().postData("api/cursos", data);
    } else {
      final id = widget.curso!["id"];
      await ApiService().putData("api/cursos/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.curso == null
            ? "Nuevo Curso"
            : "Editar Curso"),
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
              controller: nivelController,
              decoration: const InputDecoration(
                labelText: "Nivel",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: duracionController,
              decoration: const InputDecoration(
                labelText: "Duracion",
              ),
            ),
            const SizedBox(height: 12),
            

            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : saveCurso,
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
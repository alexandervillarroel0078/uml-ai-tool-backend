
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class CategoriaDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? categoria;
  const CategoriaDetailScreen({super.key, this.categoria});

  @override
  State<CategoriaDetailScreen> createState() => _CategoriaDetailScreenState();
}

class _CategoriaDetailScreenState extends State<CategoriaDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController nombreController = TextEditingController();
  
  final TextEditingController descripcionController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  
  List<dynamic> categorias = [];
  int? selectedCategoriaId;
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.categoria != null) {
      
      nombreController.text = widget.categoria!['nombre']?.toString() ?? '';
      
      descripcionController.text = widget.categoria!['descripcion']?.toString() ?? '';
      
      
      // Detectar si el backend devuelve objeto o id plano
      final relValue1 = widget.categoria!['categoria'];
      if (relValue1 is Map && relValue1['id'] != null) {
        selectedCategoriaId = relValue1['id'];
      } else if (widget.categoria!['categoria_id'] != null) {
        selectedCategoriaId = widget.categoria!['categoria_id'];
      }
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    categorias = await ApiService().getData('api/categorias') ?? [];
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> saveCategoria() async {
    setState(() => loading = true);

    final data = {
      
      "nombre": nombreController.text,
      
      "descripcion": descripcionController.text,
      
      
      "categoria": {"id": selectedCategoriaId},
      
    };

    if (widget.categoria == null) {
      await ApiService().postData("api/categorias", data);
    } else {
      final id = widget.categoria!["id"];
      await ApiService().putData("api/categorias/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.categoria == null
            ? "Nuevo Categoria"
            : "Editar Categoria"),
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
            

            
            DropdownButtonFormField<int>(
              value: selectedCategoriaId,
              decoration: InputDecoration(labelText: "Categoria"),
              items: categorias.map<DropdownMenuItem<int>>((item) {
                final label = item["nombre"] ?? item["titulo"] ?? "ID: ${item["id"]}";
                return DropdownMenuItem(value: item["id"], child: Text(label));
              }).toList(),
              onChanged: (v) => setState(() => selectedCategoriaId = v),
            ),
            const SizedBox(height: 12),
            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : saveCategoria,
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
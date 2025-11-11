
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ProductoDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? producto;
  const ProductoDetailScreen({super.key, this.producto});

  @override
  State<ProductoDetailScreen> createState() => _ProductoDetailScreenState();
}

class _ProductoDetailScreenState extends State<ProductoDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController nombreController = TextEditingController();
  
  final TextEditingController precioController = TextEditingController();
  
  final TextEditingController stockController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.producto != null) {
      
      nombreController.text = widget.producto!['nombre']?.toString() ?? '';
      
      precioController.text = widget.producto!['precio']?.toString() ?? '';
      
      stockController.text = widget.producto!['stock']?.toString() ?? '';
      
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> saveProducto() async {
    setState(() => loading = true);

    final data = {
      
      "nombre": nombreController.text,
      
      "precio": precioController.text,
      
      "stock": stockController.text,
      
      
    };

    if (widget.producto == null) {
      await ApiService().postData("api/productos", data);
    } else {
      final id = widget.producto!["id"];
      await ApiService().putData("api/productos/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.producto == null
            ? "Nuevo Producto"
            : "Editar Producto"),
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
              controller: precioController,
              decoration: const InputDecoration(
                labelText: "Precio",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: stockController,
              decoration: const InputDecoration(
                labelText: "Stock",
              ),
            ),
            const SizedBox(height: 12),
            

            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : saveProducto,
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
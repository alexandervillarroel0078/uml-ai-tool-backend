
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class FacturaDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? factura;
  const FacturaDetailScreen({super.key, this.factura});

  @override
  State<FacturaDetailScreen> createState() => _FacturaDetailScreenState();
}

class _FacturaDetailScreenState extends State<FacturaDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController fechaEmisionController = TextEditingController();
  
  final TextEditingController montoTotalController = TextEditingController();
  
  final TextEditingController metodoPagoController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.factura != null) {
      
      fechaEmisionController.text = widget.factura!['fechaEmision']?.toString() ?? '';
      
      montoTotalController.text = widget.factura!['montoTotal']?.toString() ?? '';
      
      metodoPagoController.text = widget.factura!['metodoPago']?.toString() ?? '';
      
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> saveFactura() async {
    setState(() => loading = true);

    final data = {
      
      "fechaEmision": fechaEmisionController.text,
      
      "montoTotal": montoTotalController.text,
      
      "metodoPago": metodoPagoController.text,
      
      
    };

    if (widget.factura == null) {
      await ApiService().postData("api/facturas", data);
    } else {
      final id = widget.factura!["id"];
      await ApiService().putData("api/facturas/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.factura == null
            ? "Nuevo Factura"
            : "Editar Factura"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            
            TextField(
              controller: fechaEmisionController,
              decoration: const InputDecoration(
                labelText: "Fechaemision",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: montoTotalController,
              decoration: const InputDecoration(
                labelText: "Montototal",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: metodoPagoController,
              decoration: const InputDecoration(
                labelText: "Metodopago",
              ),
            ),
            const SizedBox(height: 12),
            

            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : saveFactura,
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

import 'package:flutter/material.dart';
import '../services/api_service.dart';

class DetallePedidoDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? detallepedido;
  const DetallePedidoDetailScreen({super.key, this.detallepedido});

  @override
  State<DetallePedidoDetailScreen> createState() => _DetallePedidoDetailScreenState();
}

class _DetallePedidoDetailScreenState extends State<DetallePedidoDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController cantidadController = TextEditingController();
  
  final TextEditingController subtotalController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  
  List<dynamic> pedidos = [];
  int? selectedPedidoId;
  
  List<dynamic> productos = [];
  int? selectedProductoId;
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.detallepedido != null) {
      
      cantidadController.text = widget.detallepedido!['cantidad']?.toString() ?? '';
      
      subtotalController.text = widget.detallepedido!['subtotal']?.toString() ?? '';
      
      
      // Detectar si el backend devuelve objeto o id plano
      final relValue1 = widget.detallepedido!['pedido'];
      if (relValue1 is Map && relValue1['id'] != null) {
        selectedPedidoId = relValue1['id'];
      } else if (widget.detallepedido!['pedido_id'] != null) {
        selectedPedidoId = widget.detallepedido!['pedido_id'];
      }
      
      // Detectar si el backend devuelve objeto o id plano
      final relValue2 = widget.detallepedido!['producto'];
      if (relValue2 is Map && relValue2['id'] != null) {
        selectedProductoId = relValue2['id'];
      } else if (widget.detallepedido!['producto_id'] != null) {
        selectedProductoId = widget.detallepedido!['producto_id'];
      }
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    pedidos = await ApiService().getData('api/pedidos') ?? [];
    
    productos = await ApiService().getData('api/productos') ?? [];
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> saveDetallePedido() async {
    setState(() => loading = true);

    final data = {
      
      "cantidad": cantidadController.text,
      
      "subtotal": subtotalController.text,
      
      
      "pedido": {"id": selectedPedidoId},
      
      "producto": {"id": selectedProductoId},
      
    };

    if (widget.detallepedido == null) {
      await ApiService().postData("api/detallepedidos", data);
    } else {
      final id = widget.detallepedido!["id"];
      await ApiService().putData("api/detallepedidos/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.detallepedido == null
            ? "Nuevo DetallePedido"
            : "Editar DetallePedido"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            
            TextField(
              controller: cantidadController,
              decoration: const InputDecoration(
                labelText: "Cantidad",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: subtotalController,
              decoration: const InputDecoration(
                labelText: "Subtotal",
              ),
            ),
            const SizedBox(height: 12),
            

            
            DropdownButtonFormField<int>(
              value: selectedPedidoId,
              decoration: InputDecoration(labelText: "Pedido"),
              items: pedidos.map<DropdownMenuItem<int>>((item) {
                final label = item["nombre"] ?? item["titulo"] ?? "ID: ${item["id"]}";
                return DropdownMenuItem(value: item["id"], child: Text(label));
              }).toList(),
              onChanged: (v) => setState(() => selectedPedidoId = v),
            ),
            const SizedBox(height: 12),
            
            DropdownButtonFormField<int>(
              value: selectedProductoId,
              decoration: InputDecoration(labelText: "Producto"),
              items: productos.map<DropdownMenuItem<int>>((item) {
                final label = item["nombre"] ?? item["titulo"] ?? "ID: ${item["id"]}";
                return DropdownMenuItem(value: item["id"], child: Text(label));
              }).toList(),
              onChanged: (v) => setState(() => selectedProductoId = v),
            ),
            const SizedBox(height: 12),
            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : saveDetallePedido,
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
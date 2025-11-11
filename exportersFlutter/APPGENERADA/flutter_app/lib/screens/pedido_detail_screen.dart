
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class PedidoDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? pedido;
  const PedidoDetailScreen({super.key, this.pedido});

  @override
  State<PedidoDetailScreen> createState() => _PedidoDetailScreenState();
}

class _PedidoDetailScreenState extends State<PedidoDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController fechaController = TextEditingController();
  
  final TextEditingController estadoController = TextEditingController();
  
  final TextEditingController totalController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  
  List<dynamic> clientes = [];
  int? selectedClienteId;
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.pedido != null) {
      
      fechaController.text = widget.pedido!['fecha']?.toString() ?? '';
      
      estadoController.text = widget.pedido!['estado']?.toString() ?? '';
      
      totalController.text = widget.pedido!['total']?.toString() ?? '';
      
      
      // Detectar si el backend devuelve objeto o id plano
      final relValue1 = widget.pedido!['cliente'];
      if (relValue1 is Map && relValue1['id'] != null) {
        selectedClienteId = relValue1['id'];
      } else if (widget.pedido!['cliente_id'] != null) {
        selectedClienteId = widget.pedido!['cliente_id'];
      }
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    clientes = await ApiService().getData('api/clientes') ?? [];
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> savePedido() async {
    setState(() => loading = true);

    final data = {
      
      "fecha": fechaController.text,
      
      "estado": estadoController.text,
      
      "total": totalController.text,
      
      
      "cliente": {"id": selectedClienteId},
      
    };

    if (widget.pedido == null) {
      await ApiService().postData("api/pedidos", data);
    } else {
      final id = widget.pedido!["id"];
      await ApiService().putData("api/pedidos/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.pedido == null
            ? "Nuevo Pedido"
            : "Editar Pedido"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            
            TextField(
              controller: fechaController,
              decoration: const InputDecoration(
                labelText: "Fecha",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: estadoController,
              decoration: const InputDecoration(
                labelText: "Estado",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: totalController,
              decoration: const InputDecoration(
                labelText: "Total",
              ),
            ),
            const SizedBox(height: 12),
            

            
            DropdownButtonFormField<int>(
              value: selectedClienteId,
              decoration: InputDecoration(labelText: "Cliente"),
              items: clientes.map<DropdownMenuItem<int>>((item) {
                final label = item["nombre"] ?? item["titulo"] ?? "ID: ${item["id"]}";
                return DropdownMenuItem(value: item["id"], child: Text(label));
              }).toList(),
              onChanged: (v) => setState(() => selectedClienteId = v),
            ),
            const SizedBox(height: 12),
            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : savePedido,
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
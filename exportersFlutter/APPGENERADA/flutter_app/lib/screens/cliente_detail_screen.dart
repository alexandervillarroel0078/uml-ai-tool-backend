
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ClienteDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? cliente;
  const ClienteDetailScreen({super.key, this.cliente});

  @override
  State<ClienteDetailScreen> createState() => _ClienteDetailScreenState();
}

class _ClienteDetailScreenState extends State<ClienteDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController nombreEmpresaController = TextEditingController();
  
  final TextEditingController telefonoController = TextEditingController();
  
  final TextEditingController direccionController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.cliente != null) {
      
      nombreEmpresaController.text = widget.cliente!['nombreEmpresa']?.toString() ?? '';
      
      telefonoController.text = widget.cliente!['telefono']?.toString() ?? '';
      
      direccionController.text = widget.cliente!['direccion']?.toString() ?? '';
      
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> saveCliente() async {
    setState(() => loading = true);

    final data = {
      
      "nombreEmpresa": nombreEmpresaController.text,
      
      "telefono": telefonoController.text,
      
      "direccion": direccionController.text,
      
      
    };

    if (widget.cliente == null) {
      await ApiService().postData("api/clientes", data);
    } else {
      final id = widget.cliente!["id"];
      await ApiService().putData("api/clientes/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.cliente == null
            ? "Nuevo Cliente"
            : "Editar Cliente"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            
            TextField(
              controller: nombreEmpresaController,
              decoration: const InputDecoration(
                labelText: "Nombreempresa",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: telefonoController,
              decoration: const InputDecoration(
                labelText: "Telefono",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: direccionController,
              decoration: const InputDecoration(
                labelText: "Direccion",
              ),
            ),
            const SizedBox(height: 12),
            

            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : saveCliente,
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
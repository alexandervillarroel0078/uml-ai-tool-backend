
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class EmpleadoDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? empleado;
  const EmpleadoDetailScreen({super.key, this.empleado});

  @override
  State<EmpleadoDetailScreen> createState() => _EmpleadoDetailScreenState();
}

class _EmpleadoDetailScreenState extends State<EmpleadoDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController cargoController = TextEditingController();
  
  final TextEditingController salarioController = TextEditingController();
  
  final TextEditingController fechaContratacionController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  
  List<dynamic> departamentos = [];
  int? selectedDepartamentoId;
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.empleado != null) {
      
      cargoController.text = widget.empleado!['cargo']?.toString() ?? '';
      
      salarioController.text = widget.empleado!['salario']?.toString() ?? '';
      
      fechaContratacionController.text = widget.empleado!['fechaContratacion']?.toString() ?? '';
      
      
      // Detectar si el backend devuelve objeto o id plano
      final relValue1 = widget.empleado!['departamento'];
      if (relValue1 is Map && relValue1['id'] != null) {
        selectedDepartamentoId = relValue1['id'];
      } else if (widget.empleado!['departamento_id'] != null) {
        selectedDepartamentoId = widget.empleado!['departamento_id'];
      }
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    departamentos = await ApiService().getData('api/departamentos') ?? [];
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> saveEmpleado() async {
    setState(() => loading = true);

    final data = {
      
      "cargo": cargoController.text,
      
      "salario": salarioController.text,
      
      "fechaContratacion": fechaContratacionController.text,
      
      
      "departamento": {"id": selectedDepartamentoId},
      
    };

    if (widget.empleado == null) {
      await ApiService().postData("api/empleados", data);
    } else {
      final id = widget.empleado!["id"];
      await ApiService().putData("api/empleados/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.empleado == null
            ? "Nuevo Empleado"
            : "Editar Empleado"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            
            TextField(
              controller: cargoController,
              decoration: const InputDecoration(
                labelText: "Cargo",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: salarioController,
              decoration: const InputDecoration(
                labelText: "Salario",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: fechaContratacionController,
              decoration: const InputDecoration(
                labelText: "Fechacontratacion",
              ),
            ),
            const SizedBox(height: 12),
            

            
            DropdownButtonFormField<int>(
              value: selectedDepartamentoId,
              decoration: InputDecoration(labelText: "Departamento"),
              items: departamentos.map<DropdownMenuItem<int>>((item) {
                final label = item["nombre"] ?? item["titulo"] ?? "ID: ${item["id"]}";
                return DropdownMenuItem(value: item["id"], child: Text(label));
              }).toList(),
              onChanged: (v) => setState(() => selectedDepartamentoId = v),
            ),
            const SizedBox(height: 12),
            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : saveEmpleado,
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
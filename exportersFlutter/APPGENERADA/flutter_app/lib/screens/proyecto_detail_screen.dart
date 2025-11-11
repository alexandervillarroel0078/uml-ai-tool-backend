
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ProyectoDetailScreen extends StatefulWidget {
  final Map<String, dynamic>? proyecto;
  const ProyectoDetailScreen({super.key, this.proyecto});

  @override
  State<ProyectoDetailScreen> createState() => _ProyectoDetailScreenState();
}

class _ProyectoDetailScreenState extends State<ProyectoDetailScreen> {
  // 🧩 Controladores de texto
  
  final TextEditingController nombreController = TextEditingController();
  
  final TextEditingController fechaInicioController = TextEditingController();
  
  final TextEditingController fechaFinController = TextEditingController();
  
  final TextEditingController presupuestoController = TextEditingController();
  

  // 🔗 Relaciones ManyToOne
  

  bool loading = false;

  @override
  void initState() {
    super.initState();
    loadRelations();

    // Si se está editando, llenar los campos
    if (widget.proyecto != null) {
      
      nombreController.text = widget.proyecto!['nombre']?.toString() ?? '';
      
      fechaInicioController.text = widget.proyecto!['fechaInicio']?.toString() ?? '';
      
      fechaFinController.text = widget.proyecto!['fechaFin']?.toString() ?? '';
      
      presupuestoController.text = widget.proyecto!['presupuesto']?.toString() ?? '';
      
      
    }

  }

  // 🔄 Cargar datos relacionados (para Dropdowns)
  Future<void> loadRelations() async {
    
    setState(() {});
  }

  // 💾 Guardar o actualizar entidad
  Future<void> saveProyecto() async {
    setState(() => loading = true);

    final data = {
      
      "nombre": nombreController.text,
      
      "fechaInicio": fechaInicioController.text,
      
      "fechaFin": fechaFinController.text,
      
      "presupuesto": presupuestoController.text,
      
      
    };

    if (widget.proyecto == null) {
      await ApiService().postData("api/proyectos", data);
    } else {
      final id = widget.proyecto!["id"];
      await ApiService().putData("api/proyectos/$id", data);
    }

    setState(() => loading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.proyecto == null
            ? "Nuevo Proyecto"
            : "Editar Proyecto"),
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
              controller: fechaInicioController,
              decoration: const InputDecoration(
                labelText: "Fechainicio",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: fechaFinController,
              decoration: const InputDecoration(
                labelText: "Fechafin",
              ),
            ),
            const SizedBox(height: 12),
            
            TextField(
              controller: presupuestoController,
              decoration: const InputDecoration(
                labelText: "Presupuesto",
              ),
            ),
            const SizedBox(height: 12),
            

            

            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: loading ? null : saveProyecto,
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
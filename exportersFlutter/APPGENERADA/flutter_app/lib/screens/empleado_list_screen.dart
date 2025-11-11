
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class EmpleadoListScreen extends StatefulWidget {
  const EmpleadoListScreen({super.key});

  @override
  State<EmpleadoListScreen> createState() => _EmpleadoListScreenState();
}

class _EmpleadoListScreenState extends State<EmpleadoListScreen> {
  List<dynamic> items = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    final response = await ApiService().getData('api/empleados');
    setState(() {
      items = response ?? [];
      loading = false;
    });
  }

  Future<void> deleteItem(int id) async {
    await ApiService().deleteData('api/empleados/$id');
    fetchData();
  }

  String buildSubtitle(Map<String, dynamic> item) {
    final buffer = StringBuffer();

    
    if (item['cargo'] != null) {
      buffer.writeln('Cargo: ${item['cargo']}');
    }
    
    if (item['salario'] != null) {
      buffer.writeln('Salario: ${item['salario']}');
    }
    
    if (item['fechaContratacion'] != null) {
      buffer.writeln('Fechacontratacion: ${item['fechaContratacion']}');
    }
    

    
    if (item['departamento'] != null) {
      final relItem = item['departamento'];
      final label = relItem['nombre'] ?? relItem['titulo'] ?? 'ID: ${relItem['id']}';
      buffer.writeln('Departamento: $label');
    }
    

    return buffer.toString();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Empleados')),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          await Navigator.pushNamed(context, '/empleadoDetail');
          fetchData(); // 🔁 refresca al volver
        },
        child: const Icon(Icons.add),
      ),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: items.length,
              itemBuilder: (context, i) {
                final item = items[i];
                return Card(
                  margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  child: ListTile(
                    title: Text('ID: ${item['id']}'),
                    subtitle: Text(buildSubtitle(item)),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        IconButton(
                          icon: const Icon(Icons.edit),
                          onPressed: () async {
                            // 🔍 Obtener datos completos antes de editar
                            showDialog(
                              context: context,
                              barrierDismissible: false,
                              builder: (_) => const Center(child: CircularProgressIndicator()),
                            );

                            final fullData = await ApiService().getOne("api/empleados/${item["id"]}");
                            Navigator.pop(context); // cerrar el loading

                            if (fullData != null) {
                              await Navigator.pushNamed(
                                context,
                                '/empleadoDetail',
                                arguments: fullData,
                              );
                              fetchData(); // 🔁 refresca después de editar
                            }
                          },
                        ),


                        IconButton(
                          icon: const Icon(Icons.delete, color: Colors.red),
                          onPressed: () => deleteItem(item['id']),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
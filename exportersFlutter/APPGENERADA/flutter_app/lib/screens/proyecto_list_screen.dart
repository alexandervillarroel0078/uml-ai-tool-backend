
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ProyectoListScreen extends StatefulWidget {
  const ProyectoListScreen({super.key});

  @override
  State<ProyectoListScreen> createState() => _ProyectoListScreenState();
}

class _ProyectoListScreenState extends State<ProyectoListScreen> {
  List<dynamic> items = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    final response = await ApiService().getData('api/proyectos');
    setState(() {
      items = response ?? [];
      loading = false;
    });
  }

  Future<void> deleteItem(int id) async {
    await ApiService().deleteData('api/proyectos/$id');
    fetchData();
  }

  String buildSubtitle(Map<String, dynamic> item) {
    final buffer = StringBuffer();

    
    if (item['nombre'] != null) {
      buffer.writeln('Nombre: ${item['nombre']}');
    }
    
    if (item['fechaInicio'] != null) {
      buffer.writeln('Fechainicio: ${item['fechaInicio']}');
    }
    
    if (item['fechaFin'] != null) {
      buffer.writeln('Fechafin: ${item['fechaFin']}');
    }
    
    if (item['presupuesto'] != null) {
      buffer.writeln('Presupuesto: ${item['presupuesto']}');
    }
    

    

    return buffer.toString();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Proyectos')),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          await Navigator.pushNamed(context, '/proyectoDetail');
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

                            final fullData = await ApiService().getOne("api/proyectos/${item["id"]}");
                            Navigator.pop(context); // cerrar el loading

                            if (fullData != null) {
                              await Navigator.pushNamed(
                                context,
                                '/proyectoDetail',
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
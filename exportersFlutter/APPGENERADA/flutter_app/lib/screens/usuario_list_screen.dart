
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class UsuarioListScreen extends StatefulWidget {
  const UsuarioListScreen({super.key});

  @override
  State<UsuarioListScreen> createState() => _UsuarioListScreenState();
}

class _UsuarioListScreenState extends State<UsuarioListScreen> {
  List<dynamic> items = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    final response = await ApiService().getData('api/usuarios');
    setState(() {
      items = response ?? [];
      loading = false;
    });
  }

  Future<void> deleteItem(int id) async {
    await ApiService().deleteData('api/usuarios/$id');
    fetchData();
  }

  String buildSubtitle(Map<String, dynamic> item) {
    final buffer = StringBuffer();

    
    if (item['nombre'] != null) {
      buffer.writeln('Nombre: ${item['nombre']}');
    }
    
    if (item['email'] != null) {
      buffer.writeln('Email: ${item['email']}');
    }
    
    if (item['password'] != null) {
      buffer.writeln('Password: ${item['password']}');
    }
    

    

    return buffer.toString();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Usuarios')),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          await Navigator.pushNamed(context, '/usuarioDetail');
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

                            final fullData = await ApiService().getOne("api/usuarios/${item["id"]}");
                            Navigator.pop(context); // cerrar el loading

                            if (fullData != null) {
                              await Navigator.pushNamed(
                                context,
                                '/usuarioDetail',
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
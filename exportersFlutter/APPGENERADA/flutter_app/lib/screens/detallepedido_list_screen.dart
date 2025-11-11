
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class DetallePedidoListScreen extends StatefulWidget {
  const DetallePedidoListScreen({super.key});

  @override
  State<DetallePedidoListScreen> createState() => _DetallePedidoListScreenState();
}

class _DetallePedidoListScreenState extends State<DetallePedidoListScreen> {
  List<dynamic> items = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    fetchData();
  }

  Future<void> fetchData() async {
    final response = await ApiService().getData('api/detallepedidos');
    setState(() {
      items = response ?? [];
      loading = false;
    });
  }

  Future<void> deleteItem(int id) async {
    await ApiService().deleteData('api/detallepedidos/$id');
    fetchData();
  }

  String buildSubtitle(Map<String, dynamic> item) {
    final buffer = StringBuffer();

    
    if (item['cantidad'] != null) {
      buffer.writeln('Cantidad: ${item['cantidad']}');
    }
    
    if (item['subtotal'] != null) {
      buffer.writeln('Subtotal: ${item['subtotal']}');
    }
    

    
    if (item['pedido'] != null) {
      final relItem = item['pedido'];
      final label = relItem['nombre'] ?? relItem['titulo'] ?? 'ID: ${relItem['id']}';
      buffer.writeln('Pedido: $label');
    }
    
    if (item['producto'] != null) {
      final relItem = item['producto'];
      final label = relItem['nombre'] ?? relItem['titulo'] ?? 'ID: ${relItem['id']}';
      buffer.writeln('Producto: $label');
    }
    

    return buffer.toString();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('DetallePedidos')),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          await Navigator.pushNamed(context, '/detallepedidoDetail');
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

                            final fullData = await ApiService().getOne("api/detallepedidos/${item["id"]}");
                            Navigator.pop(context); // cerrar el loading

                            if (fullData != null) {
                              await Navigator.pushNamed(
                                context,
                                '/detallepedidoDetail',
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
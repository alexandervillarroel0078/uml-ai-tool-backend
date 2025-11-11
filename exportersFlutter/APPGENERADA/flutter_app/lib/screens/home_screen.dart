import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('🏠 Sistema Sistema Gestion Empresarial')),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          const Text(
            '📋 Tablas del UML',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('Pedido'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/pedidoList');
            },
          ),
          const SizedBox(height: 8),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('DetallePedido'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/detallepedidoList');
            },
          ),
          const SizedBox(height: 8),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('Producto'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/productoList');
            },
          ),
          const SizedBox(height: 8),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('Cliente'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/clienteList');
            },
          ),
          const SizedBox(height: 8),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('Usuario'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/usuarioList');
            },
          ),
          const SizedBox(height: 8),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('Rol'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/rolList');
            },
          ),
          const SizedBox(height: 8),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('Categoria'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/categoriaList');
            },
          ),
          const SizedBox(height: 8),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('Curso'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/cursoList');
            },
          ),
          const SizedBox(height: 8),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('Factura'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/facturaList');
            },
          ),
          const SizedBox(height: 8),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('Empleado'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/empleadoList');
            },
          ),
          const SizedBox(height: 8),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('Proyecto'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/proyectoList');
            },
          ),
          const SizedBox(height: 8),
          
          ElevatedButton.icon(
            icon: const Icon(Icons.table_chart),
            label: Text('Departamento'),
            style: ElevatedButton.styleFrom(
              minimumSize: const Size.fromHeight(48),
            ),
            onPressed: () {
              Navigator.pushNamed(context, '/departamentoList');
            },
          ),
          const SizedBox(height: 8),
          
        ],
      ),
    );
  }
}
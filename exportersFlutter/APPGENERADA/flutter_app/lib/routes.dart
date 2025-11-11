import 'package:flutter/material.dart';

import 'screens/pedido_list_screen.dart';
import 'screens/pedido_detail_screen.dart';

import 'screens/detallepedido_list_screen.dart';
import 'screens/detallepedido_detail_screen.dart';

import 'screens/producto_list_screen.dart';
import 'screens/producto_detail_screen.dart';

import 'screens/cliente_list_screen.dart';
import 'screens/cliente_detail_screen.dart';

import 'screens/usuario_list_screen.dart';
import 'screens/usuario_detail_screen.dart';

import 'screens/rol_list_screen.dart';
import 'screens/rol_detail_screen.dart';

import 'screens/categoria_list_screen.dart';
import 'screens/categoria_detail_screen.dart';

import 'screens/curso_list_screen.dart';
import 'screens/curso_detail_screen.dart';

import 'screens/factura_list_screen.dart';
import 'screens/factura_detail_screen.dart';

import 'screens/empleado_list_screen.dart';
import 'screens/empleado_detail_screen.dart';

import 'screens/proyecto_list_screen.dart';
import 'screens/proyecto_detail_screen.dart';

import 'screens/departamento_list_screen.dart';
import 'screens/departamento_detail_screen.dart';

import 'screens/login_screen.dart';
import 'screens/home_screen.dart';

final Map<String, WidgetBuilder> appRoutes = {
  '/login': (context) => const LoginScreen(),
  '/home': (context) => const HomeScreen(),
  
  '/pedidoList': (context) => const PedidoListScreen(),
  '/pedidoDetail': (context) => const PedidoDetailScreen(),
  
  '/detallepedidoList': (context) => const DetallePedidoListScreen(),
  '/detallepedidoDetail': (context) => const DetallePedidoDetailScreen(),
  
  '/productoList': (context) => const ProductoListScreen(),
  '/productoDetail': (context) => const ProductoDetailScreen(),
  
  '/clienteList': (context) => const ClienteListScreen(),
  '/clienteDetail': (context) => const ClienteDetailScreen(),
  
  '/usuarioList': (context) => const UsuarioListScreen(),
  '/usuarioDetail': (context) => const UsuarioDetailScreen(),
  
  '/rolList': (context) => const RolListScreen(),
  '/rolDetail': (context) => const RolDetailScreen(),
  
  '/categoriaList': (context) => const CategoriaListScreen(),
  '/categoriaDetail': (context) => const CategoriaDetailScreen(),
  
  '/cursoList': (context) => const CursoListScreen(),
  '/cursoDetail': (context) => const CursoDetailScreen(),
  
  '/facturaList': (context) => const FacturaListScreen(),
  '/facturaDetail': (context) => const FacturaDetailScreen(),
  
  '/empleadoList': (context) => const EmpleadoListScreen(),
  '/empleadoDetail': (context) => const EmpleadoDetailScreen(),
  
  '/proyectoList': (context) => const ProyectoListScreen(),
  '/proyectoDetail': (context) => const ProyectoDetailScreen(),
  
  '/departamentoList': (context) => const DepartamentoListScreen(),
  '/departamentoDetail': (context) => const DepartamentoDetailScreen(),
  
};
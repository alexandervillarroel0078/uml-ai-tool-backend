import 'package:flutter/material.dart';
import 'routes.dart';
import 'screens/login_screen.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'UML Generated App',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const LoginScreen(),
      routes: appRoutes,
    );
  }
}
exportersFlutter/
 ┣ generators/
 ┃ ┣ flutter_generator.py          ← coordina todo el flujo de generación
 ┃ ┣ json_to_flutter_model.py      ← traduce clases UML a modelos Dart
 ┃ ┣ json_to_flutter_service.py    ← crea archivo de conexión API (http)
 ┃ ┣ json_to_flutter_ui.py         ← crea pantallas (List/Detail)
 ┃ ┗ project_builder_flutter.py    ← crea carpetas base del proyecto
 ┣ templates/
 ┃ ┣ main.dart.j2
 ┃ ┣ routes.dart.j2
 ┃ ┣ pubspec.yaml.j2
 ┃ ┣ api_service.dart.j2
 ┃ ┣ model.dart.j2
 ┃ ┣ screen_list.dart.j2
 ┃ ┣ screen_detail.dart.j2
 ┃ ┗ README.md.j2
 ┣ __init__.py                     ← opcional (si lo quieres como módulo Python)
 ┗ README.md                       ← documentación del generador


cd exportersFlutter


cd uml-ai-tool-backend
.venv\Scripts\Activate.ps1



 

Remove-Item -Recurse -Force "C:\xampp\htdocs\sw1\uml-ai-tool-backend\exportersFlutter\APPGENERADA"

python exportersFlutter/generators/flutter_generator.py
cd C:\xampp\htdocs\sw1\uml-ai-tool-backend\exportersFlutter\APPGENERADA\flutter_app
flutter pub get
flutter devices
flutter run -d chrome



SELECT * FROM public.usuario
ORDER BY id ASC 

SELECT * FROM detalle_pedido;
SELECT * FROM pedido;
SELECT * FROM cliente;

INSERT INTO usuario (email, nombre, password)
VALUES ('admin@demo.com', 'Admin', '1234');

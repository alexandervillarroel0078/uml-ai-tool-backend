class Departamento {
  
  final String id;
  
  final String nombre;
  
  final String ubicacion;
  

  Departamento({ required this.id, required this.nombre, required this.ubicacion,  });

  factory Departamento.fromJson(Map<String, dynamic> json) => Departamento(
    
    id: json['id'],
    
    nombre: json['nombre'],
    
    ubicacion: json['ubicacion'],
    
  );

  Map<String, dynamic> toJson() => {
    
    'id': id,
    
    'nombre': nombre,
    
    'ubicacion': ubicacion,
    
  };
}
class Rol {
  
  final String id;
  
  final String nombre;
  
  final String descripcion;
  

  Rol({ required this.id, required this.nombre, required this.descripcion,  });

  factory Rol.fromJson(Map<String, dynamic> json) => Rol(
    
    id: json['id'],
    
    nombre: json['nombre'],
    
    descripcion: json['descripcion'],
    
  );

  Map<String, dynamic> toJson() => {
    
    'id': id,
    
    'nombre': nombre,
    
    'descripcion': descripcion,
    
  };
}
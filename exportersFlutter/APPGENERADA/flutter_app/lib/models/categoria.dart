class Categoria {
  
  final String id;
  
  final String nombre;
  
  final String descripcion;
  

  Categoria({ required this.id, required this.nombre, required this.descripcion,  });

  factory Categoria.fromJson(Map<String, dynamic> json) => Categoria(
    
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
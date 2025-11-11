class Curso {
  
  final String id;
  
  final String nombre;
  
  final String nivel;
  
  final int duracion;
  

  Curso({ required this.id, required this.nombre, required this.nivel, required this.duracion,  });

  factory Curso.fromJson(Map<String, dynamic> json) => Curso(
    
    id: json['id'],
    
    nombre: json['nombre'],
    
    nivel: json['nivel'],
    
    duracion: json['duracion'],
    
  );

  Map<String, dynamic> toJson() => {
    
    'id': id,
    
    'nombre': nombre,
    
    'nivel': nivel,
    
    'duracion': duracion,
    
  };
}
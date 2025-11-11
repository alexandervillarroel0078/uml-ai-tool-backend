class Proyecto {
  
  final String id;
  
  final String nombre;
  
  final DateTime fechaInicio;
  
  final DateTime fechaFin;
  
  final double presupuesto;
  

  Proyecto({ required this.id, required this.nombre, required this.fechaInicio, required this.fechaFin, required this.presupuesto,  });

  factory Proyecto.fromJson(Map<String, dynamic> json) => Proyecto(
    
    id: json['id'],
    
    nombre: json['nombre'],
    
    fechaInicio: json['fechaInicio'],
    
    fechaFin: json['fechaFin'],
    
    presupuesto: json['presupuesto'],
    
  );

  Map<String, dynamic> toJson() => {
    
    'id': id,
    
    'nombre': nombre,
    
    'fechaInicio': fechaInicio,
    
    'fechaFin': fechaFin,
    
    'presupuesto': presupuesto,
    
  };
}
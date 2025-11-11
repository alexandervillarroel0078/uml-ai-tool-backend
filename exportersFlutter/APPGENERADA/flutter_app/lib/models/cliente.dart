class Cliente {
  
  final String id;
  
  final String nombreEmpresa;
  
  final String telefono;
  
  final String direccion;
  

  Cliente({ required this.id, required this.nombreEmpresa, required this.telefono, required this.direccion,  });

  factory Cliente.fromJson(Map<String, dynamic> json) => Cliente(
    
    id: json['id'],
    
    nombreEmpresa: json['nombreEmpresa'],
    
    telefono: json['telefono'],
    
    direccion: json['direccion'],
    
  );

  Map<String, dynamic> toJson() => {
    
    'id': id,
    
    'nombreEmpresa': nombreEmpresa,
    
    'telefono': telefono,
    
    'direccion': direccion,
    
  };
}
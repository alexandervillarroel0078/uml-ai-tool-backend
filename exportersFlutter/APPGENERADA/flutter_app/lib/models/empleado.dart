class Empleado {
  
  final String id;
  
  final String cargo;
  
  final double salario;
  
  final DateTime fechaContratacion;
  

  Empleado({ required this.id, required this.cargo, required this.salario, required this.fechaContratacion,  });

  factory Empleado.fromJson(Map<String, dynamic> json) => Empleado(
    
    id: json['id'],
    
    cargo: json['cargo'],
    
    salario: json['salario'],
    
    fechaContratacion: json['fechaContratacion'],
    
  );

  Map<String, dynamic> toJson() => {
    
    'id': id,
    
    'cargo': cargo,
    
    'salario': salario,
    
    'fechaContratacion': fechaContratacion,
    
  };
}
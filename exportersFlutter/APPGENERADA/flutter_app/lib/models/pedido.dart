class Pedido {
  
  final String id;
  
  final DateTime fecha;
  
  final String estado;
  
  final double total;
  

  Pedido({ required this.id, required this.fecha, required this.estado, required this.total,  });

  factory Pedido.fromJson(Map<String, dynamic> json) => Pedido(
    
    id: json['id'],
    
    fecha: json['fecha'],
    
    estado: json['estado'],
    
    total: json['total'],
    
  );

  Map<String, dynamic> toJson() => {
    
    'id': id,
    
    'fecha': fecha,
    
    'estado': estado,
    
    'total': total,
    
  };
}
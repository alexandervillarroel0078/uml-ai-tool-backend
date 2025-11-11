class DetallePedido {
  
  final String id;
  
  final int cantidad;
  
  final double subtotal;
  

  DetallePedido({ required this.id, required this.cantidad, required this.subtotal,  });

  factory DetallePedido.fromJson(Map<String, dynamic> json) => DetallePedido(
    
    id: json['id'],
    
    cantidad: json['cantidad'],
    
    subtotal: json['subtotal'],
    
  );

  Map<String, dynamic> toJson() => {
    
    'id': id,
    
    'cantidad': cantidad,
    
    'subtotal': subtotal,
    
  };
}
class Factura {
  
  final String id;
  
  final DateTime fechaEmision;
  
  final double montoTotal;
  
  final String metodoPago;
  

  Factura({ required this.id, required this.fechaEmision, required this.montoTotal, required this.metodoPago,  });

  factory Factura.fromJson(Map<String, dynamic> json) => Factura(
    
    id: json['id'],
    
    fechaEmision: json['fechaEmision'],
    
    montoTotal: json['montoTotal'],
    
    metodoPago: json['metodoPago'],
    
  );

  Map<String, dynamic> toJson() => {
    
    'id': id,
    
    'fechaEmision': fechaEmision,
    
    'montoTotal': montoTotal,
    
    'metodoPago': metodoPago,
    
  };
}
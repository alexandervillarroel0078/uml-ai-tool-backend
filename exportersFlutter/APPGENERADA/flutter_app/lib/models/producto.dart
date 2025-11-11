class Producto {
  
  final String id;
  
  final String nombre;
  
  final double precio;
  
  final int stock;
  

  Producto({ required this.id, required this.nombre, required this.precio, required this.stock,  });

  factory Producto.fromJson(Map<String, dynamic> json) => Producto(
    
    id: json['id'],
    
    nombre: json['nombre'],
    
    precio: json['precio'],
    
    stock: json['stock'],
    
  );

  Map<String, dynamic> toJson() => {
    
    'id': id,
    
    'nombre': nombre,
    
    'precio': precio,
    
    'stock': stock,
    
  };
}
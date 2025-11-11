import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  // ✅ Backend corriendo en Spring Boot local
  final String baseUrl = "http://localhost:8080";

  Future<List<dynamic>?> getData(String endpoint) async {
    final res = await http.get(Uri.parse('$baseUrl/$endpoint'));
    if (res.statusCode == 200) return jsonDecode(res.body);
    print("❌ Error GET ${res.statusCode}");
    return null;
  }
  Future<Map<String, dynamic>?> getOne(String endpoint) async {
    final res = await http.get(Uri.parse('$baseUrl/$endpoint'));
    if (res.statusCode == 200) {
      return jsonDecode(res.body) as Map<String, dynamic>;
    }
    print("❌ Error GET one ${res.statusCode}");
    return null;
  }
  Future<Map<String, dynamic>?> postData(String endpoint, Map<String, dynamic> body) async {
    final res = await http.post(
      Uri.parse('$baseUrl/$endpoint'),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(body),
    );
    if (res.statusCode == 200 || res.statusCode == 201) return jsonDecode(res.body);
    print("❌ Error POST ${res.statusCode}");
    return null;
  }

  Future<Map<String, dynamic>?> putData(String endpoint, Map<String, dynamic> body) async {
    final res = await http.put(
      Uri.parse('$baseUrl/$endpoint'),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(body),
    );
    if (res.statusCode == 200) return jsonDecode(res.body);
    print("❌ Error PUT ${res.statusCode}");
    return null;
  }

  Future<void> deleteData(String endpoint) async {
    final res = await http.delete(Uri.parse('$baseUrl/$endpoint'));
    if (res.statusCode != 200 && res.statusCode != 204) {
      print("❌ Error DELETE ${res.statusCode}");
    }
  }
}
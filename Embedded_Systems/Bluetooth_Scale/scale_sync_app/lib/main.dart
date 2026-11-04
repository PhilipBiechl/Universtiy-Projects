import 'package:flutter/material.dart';
import 'package:scale_sync_app/Views/main_view.dart';

void main() async {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      /*  Initialise App with no Debug-Banner on Screen
          and MainView() as default screen  */
      debugShowCheckedModeBanner: false,
      home: MainView(),
    );
  }
}
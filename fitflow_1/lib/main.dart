import 'package:flutter/material.dart';
import 'selection_screen.dart'; // Assuming this is where ExerciseSelectionScreen is defined

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // Wrap with MaterialApp
      title: 'FitFlow',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: ExerciseSelectionScreen(), // Your main screen
    );
  }
}

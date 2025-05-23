import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'camera_screen.dart'; // Import CameraScreen

//Image assets
const bicepCurlImagePath = 'lib/assets/img/bicep.jpg';
const basicPlankImagePath = 'lib/assets/img/plank.jpg';
const basicSquatImagePath = 'lib/assets/img/squat.jpg';
const lungeImagePath = 'lib/assets/img/lunge.jpg';

class ExerciseSelectionScreen extends StatefulWidget {
  const ExerciseSelectionScreen({super.key});

  @override
  _ExerciseSelectionScreenState createState() =>
      _ExerciseSelectionScreenState();
}

class _ExerciseSelectionScreenState extends State<ExerciseSelectionScreen> {
  String? _selectedExercise;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Choose The Exercise')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            ExerciseTile(
              exercise: 'Bicep Curl',
              imagePath: bicepCurlImagePath,
              isSelected: _selectedExercise == 'Bicep Curl',
              onTap: () {
                _selectExercise('Bicep Curl');
                _navigateToCameraScreen(context, 'Bicep Curl');
              },
            ),
            ExerciseTile(
              exercise: 'Basic Plank',
              imagePath: basicPlankImagePath,
              isSelected: _selectedExercise == 'Basic Plank',
              onTap: () {
                _selectExercise('Basic Plank');
                _navigateToCameraScreen(context, 'Basic Plank');
              },
            ),
            ExerciseTile(
              exercise: 'Basic Squat',
              imagePath: basicSquatImagePath,
              isSelected: _selectedExercise == 'Basic Squat',
              onTap: () {
                _selectExercise('Basic Squat');
                _navigateToCameraScreen(context, 'Basic Squat');
              },
            ),
            ExerciseTile(
              exercise: 'Lunge',
              imagePath: lungeImagePath,
              isSelected: _selectedExercise == 'Lunge',
              onTap: () {
                _selectExercise('Lunge');
                _navigateToCameraScreen(context, 'Lunge');
              },
            ),
          ],
        ),
      ),
    );
  }

  void _selectExercise(String exercise) {
    setState(() {
      _selectedExercise = exercise;
    });
  }

  void _navigateToCameraScreen(BuildContext context, String exercise) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => CameraScreen(exercise: exercise)),
    );
  }
}

class ExerciseTile extends StatelessWidget {
  final String exercise;
  final String imagePath;
  final bool isSelected;
  final VoidCallback onTap;

  const ExerciseTile({
    super.key,
    required this.exercise,
    required this.imagePath,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: isSelected ? Colors.grey[300] : null, // Highlight selection
      shape: RoundedRectangleBorder(
        side:
            isSelected
                ? BorderSide(color: Colors.black, width: 2)
                : BorderSide.none,
        borderRadius: BorderRadius.circular(8.0),
      ),
      child: ListTile(
        leading: Image.asset(imagePath, width: 40, height: 40),
        title: Text(
          exercise,
          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
        ),
        trailing: isSelected ? const Icon(Icons.check) : null,
        onTap: onTap,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8.0)),
      ),
    );
  }
}

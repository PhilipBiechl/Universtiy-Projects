import 'package:flutter/material.dart';
import '../DataAndValues/data_value.dart';
import '../Controller/data_controller.dart';

/*  Paint hand of scale  */
class ScaleHandPainter extends CustomPainter{
  final Paint scaleHandPaint;
  double gramms;

  ScaleHandPainter({this.gramms = 0})
      :scaleHandPaint = Paint()
  {
    scaleHandPaint.color= const Color(0xFF333333);
    scaleHandPaint.style= PaintingStyle.fill;
  }

  @override
  void paint(Canvas canvas, Size size) {
    final angle = -(2 * 3.1415 / 3) + (gramms * 2 * 2 * 3.1415) / (range * 3);
    const radius = 75.0;

    canvas.save();

    canvas.translate(radius+37.5, radius+37.5);
    canvas.rotate(angle);

    Path path = Path();
    path.moveTo(-1.5, -radius-10.0);
    path.lineTo(-3.0, -radius/1.8);
    path.lineTo(-2.0, 10.0);
    path.lineTo(2.0, 10.0);
    path.lineTo(3.0, -radius/1.8);
    path.lineTo(1.5, -radius-10.0);
    path.close();

    canvas.drawPath(path, scaleHandPaint);
    canvas.drawShadow(path, Colors.black, 4.0, false);

    canvas.restore();
  }
  @override
  bool shouldRepaint(ScaleHandPainter oldDelegate) {
    return true;
  }
}

/*  Paint the scale numbers etc.  */
class ScalePainter extends CustomPainter {
  final tenthsTickMarkLength = 10.0;
  final singleTickMarkLength = 5.0;
  final tenthsTickMarkWidth = 3.0;
  final singleTickMarkWidth = 1.5;

  final Paint tickPaint;
  final TextPainter textPainter;
  final TextStyle textStyle;

  ScalePainter()
      :tickPaint= Paint(),
        textPainter= TextPainter(
          textAlign: TextAlign.center,
          textDirection: TextDirection.rtl,
        ),
        textStyle= const TextStyle(
          color: Colors.black,
          fontFamily: 'Times New Roman',
          fontSize: 15.0,
        )
  {
    tickPaint.color= Colors.blueGrey;
  }

  @override
  void paint(Canvas canvas, Size size) {
    var tickMarkLength = 0.0;
    final angle = (2 * 2 * 3.1415) / (range * 3);
    final radius = size.width / 2;
    canvas.save();

    canvas.translate(radius, radius);
    canvas.rotate(-(2 * 3.1415 / 3));
    for (var i = 0; i <= range; i++) {
      tickMarkLength = i % (range / 10) == 0 ? tenthsTickMarkLength: singleTickMarkLength;
      tickPaint.strokeWidth= i % (range / 10) == 0 ? tenthsTickMarkWidth : singleTickMarkWidth;
      canvas.drawLine(
          Offset(0.0, -radius), Offset(0.0, -radius+tickMarkLength), tickPaint);

      if (i % (range / 10) == 0) {
        canvas.save();
        canvas.translate(0.0, -radius+25.0);
        canvas.rotate(2.1);

        textPainter.text= TextSpan(
          text: i.toString(),
          style: textStyle,
        );

        canvas.rotate(-angle * i);
        textPainter.layout();
        textPainter.paint(canvas, Offset(-(textPainter.width/2), -(textPainter.height/2)));
        canvas.restore();
      }
      canvas.rotate(angle);
    }
    canvas.restore();
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) {
    return false;
  }
}

/*  Paint the background of the scale and face on it  */
class ScaleOnFace extends StatelessWidget{
  const ScaleOnFace({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(10.0),
      child: AspectRatio(
        aspectRatio: 1.0,
        child: Container(
          width: double.infinity,
          decoration: const BoxDecoration(
            shape: BoxShape.circle,
            color: Colors.white,
          ),
          child: Stack(
            children: <Widget>[
              Container(
                width: double.infinity,
                height: double.infinity,
                padding: const EdgeInsets.all(10.0),
                /*  ScalePainter is on top of painted circle  */
                child: CustomPaint(
                  painter: ScalePainter(),
                ),
              ),
              Center(
                child: Container(
                  width: 15.0,
                  height: 15.0,
                  decoration: const BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.black,
                  ),
                ),
              ),
              CustomPaint(painter: ScaleHandPainter(gramms: scaleMeasure)),
              Container(
                  width: double.infinity,
                  height: double.infinity,
                  margin: EdgeInsets.only(
                      top: MediaQuery.of(context).size.height * 0.175,
                      bottom: MediaQuery.of(context).size.height * 0.025,
                      left: MediaQuery.of(context).size.width * 0.15,
                      right: MediaQuery.of(context).size.width * 0.15
                  ),
                  decoration: BoxDecoration(
                    color: const Color.fromRGBO(20, 20, 20, 80),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  padding: const EdgeInsets.all(10.0),
                  child: Center(
                    child: Text(
                      '${scaleMeasure.toStringAsFixed(2)} g',
                      style: const TextStyle(
                          color: Colors.redAccent,
                          fontWeight: FontWeight.w600,
                          letterSpacing: 2,
                          fontSize: 15
                      ),
                    ),
                  )
              ),
            ],
          ),
        ),
      ),
    );
  }
}

/*  Paint sectors behind the scale  */
class SectorsPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final Paint paint = Paint()
      ..isAntiAlias = true
      ..strokeWidth = 3.0
      ..style = PaintingStyle.fill;

    final arcsRect = Rect.fromLTWH(
        mainScaleFace['outerLeft']!,
        mainScaleFace['outerTop']!,
        mainScaleFace['outerRadius']!,
        mainScaleFace['outerRadius']!
    );
    const useCenter = true;

    List<Color> sectorColors = [
      Colors.blue,
      Colors.red,
      Colors.yellow,
      Color.fromRGBO(0, 0, 0, 0),
      Color.fromRGBO(0, 0, 0, 0),
      Color.fromRGBO(0, 0, 0, 0)
    ];

    scaleNeeded = currentRecipe == 0 ? 0 : int.parse(gSteps[currentStep]['mass_for_scale']);

    double sweepAngle = (0.628319-0.026) * 7 / range;
    double startAngle = 2.513274+0.09;
    for(int i = 0; i < scaleMeasure; i++) {
      canvas.drawArc(arcsRect, startAngle, sweepAngle, useCenter,
          paint..color = sectorColors[0]);
      startAngle = startAngle + sweepAngle;
    }
    if (scaleMeasure <= scaleNeeded) {
      for(int i = 0; i < scaleNeeded-scaleMeasure; i++) {
        canvas.drawArc(arcsRect, startAngle, sweepAngle, useCenter,
            paint..color = sectorColors[1]);
        startAngle = startAngle + sweepAngle;
      }
    } else {
      for(int i = 0; i > scaleNeeded-scaleMeasure; i--) {
        canvas.drawArc(arcsRect, startAngle, sweepAngle, useCenter,
            paint..color = sectorColors[2]);
        startAngle = startAngle - sweepAngle;
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return false;
  }
}

/*  General Function to complete whole paint-process  */
class ScaleBody extends StatelessWidget{
  const ScaleBody({super.key});

  @override
  Widget build(BuildContext context) {
    final ValueNotifier<double> act = ValueNotifier<double>(scaleMeasure);
    return AspectRatio(
        aspectRatio: 1.0,
        child: Stack(
          alignment: const Alignment(0.0, -2.5),
          children: <Widget>[
            ValueListenableBuilder(
                valueListenable: act,
                builder: (BuildContext context, double act, Widget? child) {
                  return Container(
                    width: MediaQuery
                        .of(context)
                        .size
                        .width * 0.6,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: Color.fromRGBO(0, 0, 0, 0.3),
                    ),
                    child: const ScaleOnFace(),
                  );
                }
            ),
          ],
        )
    );
  }
}
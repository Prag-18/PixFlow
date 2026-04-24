import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:feed/main.dart';

void main() {
  testWidgets('Counter increments smoke test', (WidgetTester tester) async {
    // Build the app
    await tester.pumpWidget(const FeedApp());

    // Verify initial state
    expect(find.text('0'), findsOneWidget);
    expect(find.text('1'), findsNothing);

    // Tap the add icon
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    // Verify incremented state
    expect(find.text('0'), findsNothing);
    expect(find.text('1'), findsOneWidget);
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import '../lib/main.dart';

void main() {
  testWidgets('FeedApp smoke test - renders without crashing',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(child: FeedApp()),
    );

    // Verify the app widget tree is present
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}

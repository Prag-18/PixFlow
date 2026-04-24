# PixFlow

PixFlow is a high-performance, modern, dark-themed social feed application built with Flutter, Riverpod, and Supabase. It features smooth scrolling, dynamic UI updates, and a fully functional backend integration.

## ✨ Features

- **Premium Dark-Themed UI:** A polished, modern dark aesthetic with glassmorphic elements and seamless navigation.
- **High-Performance Rendering:** Implements `RepaintBoundary` to cache shadow rasterization and complex UI elements, minimizing GPU strain and ensuring 60fps scrolling.
- **Optimized Image Decoding:** Actively manages RAM by downscaling images using `memCacheWidth` to prevent Out-Of-Memory (OOM) errors on image-heavy screens.
- **State Management:** Fully integrated with Riverpod for robust, scalable state management, including optimistic UI updates for instant user feedback (e.g., liking posts).
- **Backend Infrastructure:** Powered by Supabase for database management, authentication, and fast edge-storage for media.
- **Dynamic Profile & Feed:** Features a 3-column photo grid and robust data layer to fetch and display user statistics seamlessly.

## 📁 Project Structure

- `feed/` - The main Flutter application directory.
  - `lib/` - Core application logic, structured into `models`, `providers`, `screens`, `services`, and `widgets`.
  - `test/` - Comprehensive widget and unit tests.
  - `seed.py` - A Python script used to process and upload seed data to Supabase.

## 🚀 Getting Started

### Prerequisites

- [Flutter SDK](https://docs.flutter.dev/get-started/install) (latest stable version)
- A Supabase Project (Database & Storage)
- Python 3.x (Optional, for running the `seed.py` data population script)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd PixFlow/feed
   ```

2. **Install dependencies:**
   ```bash
   flutter pub get
   ```

3. **Configure Environment:**
   Ensure your Supabase URL and Anon Key are correctly set up in the `lib/app_config.dart` file (or your respective environment configuration).

4. **Run the App:**
   ```bash
   flutter run
   ```

## 🛠 Tech Stack

- **Frontend:** Flutter & Dart
- **State Management:** Riverpod
- **Backend as a Service:** Supabase (PostgreSQL, Storage, RPCs)
- **Image Processing (Scripts):** Python (Pillow)

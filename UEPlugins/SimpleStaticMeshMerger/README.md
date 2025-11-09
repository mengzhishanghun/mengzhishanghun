# SimpleStaticMeshMerger Plugin

## 📖 Introduction

SimpleStaticMeshMerger is a lightweight Unreal Engine editor tool plugin designed to merge duplicate StaticMeshActors in scenes into Instance Static Mesh (ISM) or Hierarchical Instance Static Mesh (HISM), significantly improving rendering performance. The plugin provides an intuitive visual interface with real-time preview, flexible filtering, and smart search capabilities.

---

## 🔧 Core Features

- 🎯 Auto Grouping: Intelligently groups by Mesh, Mobility, Collision Settings, and Materials
- 👁️ Real-time Preview: Left panel shows merge groups, right panel displays instances
- 🔍 Fuzzy Search: Supports tokenized sequential search for quick instance location
- ⚙️ Flexible Filtering: Filter by Mobility types (Static/Stationary/Movable)
- 📊 Min Instance Count: Customize merge threshold to filter out small groups
- 🏗️ LevelInstance Support: One-click recursive breaking of nested LevelInstances
- ✅ Full Collision Preservation: Accurately copies collision profiles, object types, and all channel responses
- 🎮 Editor Integration: Dockable window with Undo/Redo support
- 🚀 Auto Navigation: Automatically selects and jumps to newly created Actors after merge

---

## 📝 Usage

### Typical Use Cases

- 🌲 Scene Optimization: Merge large quantities of trees, rocks, grass and other repeated static meshes
- 🏙️ Urban Scenes: Merge streetlights, railings, road signs and other identical models
- 🎨 Level Design: Quickly optimize scene Draw Calls

### ⚠️ Important Notes

- **Use Case**: Primarily for pre-packaging optimization to reduce loading stutters (limited FPS improvement)
- **Backup Before Use**: Merge operations are irreversible, always backup your project or use version control before merging

---

## 📚 Documentation

Step-by-step usage instructions and blueprint examples are available in:

https://github.com/mengzhishanghun/mengzhishanghun/blob/main/UEPlugins/SimpleStaticMeshMerger/Docs/README.md

---

## 📂 Author

Copyright (c) 2025
Author: mengzhishanghun
Contact: mengzhishanghun@outlook.com

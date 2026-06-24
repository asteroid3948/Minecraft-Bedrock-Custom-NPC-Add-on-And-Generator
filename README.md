# Minecraft Bedrock Custom NPC Add-on & Generator

A dynamic, script-powered Minecraft Bedrock Add-on system that allows you to create, edit, and program custom NPCs in-game. It includes a command-line utility (`packbuilder.py`) to automatically build and package a custom `.mcaddon` with any folder of skins you provide.

## Features

### In-Game Add-on Features
*   **Custom Geometry & Animation**: Features flared arms humanoid geometry and idle animations.
*   **§gNPC Creator**: Use this tool on any block to spawn a custom NPC.
*   **§gNPC Editor**: Interact with any spawned NPC with this tool to customize it on the fly.
*   **§gSet NPC Rotation**: Interact with an NPC with this tool to set its rotation. Snaps to the closest cardinal direction (North, East, South, West) if locked direction is enabled.
*   **Dual-Line Holograms**: Floating text above the NPC's head with support for 2 separate lines or combined multiline text using a custom, invulnerable floating text entity (`asteroid:floating_text`).
*   **Interactive Behaviors**: 
    *   **Fixed**: NPC stands facing a set direction (snapped or manual).
    *   **Look at Player**: NPC dynamically rotates to track the closest player within a 10-block radius.
*   **Custom Event Triggers (Commands)**:
    *   **Interact Action**: Executes one or more commands (semicolon-separated) when a player right-clicks/interacts with the NPC.
    *   **Punch Action**: Executes one or more commands (semicolon-separated) when a player punches/attacks the NPC.
    *   *Note: Commands are executed via scripting API under server console privileges. This allows **non-OP players** to trigger commands like `/gamemode`, `/give`, or `/tp` through the NPC. The script automatically replaces `@s` and `@p` with the interacting player's name.*

---

## Add-on Installation Guide
1. Download or generate the `Asteroid_NPCs.mcaddon` file.
2. Double-click the `.mcaddon` file to automatically import both the Resource Pack and Behavior Pack into Minecraft Bedrock Edition.
3. Apply both the **Asteroid Npc's BP** and **Asteroid Npc's RP** to your Minecraft world.
4. **IMPORTANT**: Make sure to enable **Beta APIs** under the Experiments tab in your world settings, as this addon relies on script events.

---

## In-Game Guide

### Spawning an NPC
1. Get the **§gNPC Creator** item from the Creative Inventory (Equipment category) or run `/give @s asteroid:npc_creator`.
2. Use/right-click on a block to open the NPC Creator UI.
3. Configure your NPC (holograms, skins, behaviors) and submit.

### Editing an NPC
1. Get the **§gNPC Editor** item from the Creative Inventory or run `/give @s asteroid:npc_editor`.
2. Right-click/interact with an existing NPC to reopen the customization form.

### Rotating & Snapping NPCs
1. Get the **§gSet NPC Rotation** wand from the Creative Inventory or run `/give @s asteroid:npc_rotator`.
2. Stand in the direction you want the NPC to face.
3. Right-click/interact with the NPC using the wand.
    *   If **Lock facing straight** is toggled **Off**, the NPC will face directly away from you (facing the same direction you are).
    *   If **Lock facing straight** is toggled **On**, the NPC will automatically snap to the nearest cardinal direction (North, East, South, or West) relative to where you are standing.
    *   *Note: When using the rotation wand, you may need to click the NPC a few times for it to fully register the rotation.*

---

## Using the Addon Generator (`packbuilder.py`)

If you want to create a custom addon using your own set of skin textures, you can use the command-line utility. The utility takes a folder of `.png` skins, indexes them, decodes the default pack icon on the fly, and packages everything into a ready-to-import `.mcaddon` file.

### Prerequisites
*   Python 3.x installed on your computer.

### Running the Builder

#### 1. Interactive Mode (Recommended)
Simply run the script with no arguments:
```bash
python packbuilder.py
```
The script will display the title, ask you to input/paste the folder path containing your skin PNGs, and let you type a custom output name.

#### 2. Command Line Mode
You can specify the skins folder and custom output name as command-line arguments:
```bash
python packbuilder.py "C:\Path\To\Skins" --output "MyCustomNpcs"
```

### Skin File Naming Guide
*   Ensure all your skins are `.png` images.
*   Place them inside a dedicated folder.
*   The script automatically sorts the images alphabetically, indexes them, and maps them to `Skin 1`, `Skin 2`, etc. in the NPC Creator UI.

---

## Technical Details

*   **Scripting Entry**: `scripts/main.js` using `@minecraft/server` and `@minecraft/server-ui`.
*   **Properties**: Syncs texture indexes through `asteroid:skin_variant` and behavior toggles through `asteroid:look_at_player`.
*   **Floating Texts**: Relies on dynamic property mappings linked via tag identifiers `npc_id_${npc.id}` on invulnerable custom entities.
*   **Commands**: Ran directly as server console using `system.runCommandAsync` with regex replacement on target selectors:
    *   `@s` -> `"PlayerName"`
    *   `@p` -> `"PlayerName"`

---

## Credits
*   **Add-on Creator**: Asteroid3948

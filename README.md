# Asteroid NPCs

Asteroid NPCs is a Minecraft Bedrock edition add-on that provides creators with tools to spawn and customize stationary, invulnerable humanoid NPCs. The system supports custom action bindings for interactions and punches, dynamic player-tracking rotation, and offset floating text holograms.

## Technical Overview

The add-on is split into a Behavior Pack (BP) and a Resource Pack (RP). Scripting is handled via the Bedrock Script API (`@minecraft/server` and `@minecraft/server-ui`).

### Entity Architecture

* **asteroid:custom_npc**: The main NPC entity. 
  * It has physics enabled with collision, but gravity and pushability components are configured to prevent movement.
  * Damage sensors are set to negate all incoming damage causes, preventing the NPC from taking damage or reacting to hits visually, while still firing hit events in the script.
  * Features custom animations mapping to the humanoid model (specifically flared arm idle configurations).
* **asteroid:floating_text**: An invisible dummy entity used to render name tags at exact offsets above the NPC's head. Spawning holograms on a separate entity avoids rendering issues and allows stacking multiple lines cleanly.

### Configuration Storage

NPC configurations are stored directly on the entity instances using dynamic properties:
* `hologram_l1` (string): Text for the first line of the hologram.
* `hologram_l2` (string): Text for the second line of the hologram.
* `hologram_combined` (boolean): Flag determining if the lines are merged on a single entity using a newline escape (`\n`) or split across two separate entities at stacked offsets.
* `behavior_type` (integer): `0` for fixed facing angle, `1` for active player tracking.
* `interact_action` (string): Command line string executed when a player interacts with the NPC.
* `punch_action` (string): Command line string executed when a player punches the NPC.

---

## Creator Tools

The add-on adds three items to the equipment category in a custom creative tab:

* **NPC Creator (asteroid:npc_creator)**: Right-clicking with this item triggers a block raycast up to 10 blocks away. It spawns the NPC centered on the targeted block and opens the configuration GUI.
* **NPC Editor (asteroid:npc_editor)**: Right-clicking an NPC with this item reads its stored dynamic properties and opens the configuration GUI pre-populated with those values.
* **Set NPC Rotation (asteroid:npc_rotator)**: Right-clicking an NPC configured in "Fixed" mode with this item calculates the horizontal angle between the NPC and the player, rotating the NPC to face the player's coordinate.

---

## Configuration Guide

When using the Creator or Editor tools, a form will open with the following options:

### Combined Lines
* **Enabled**: Merges Hologram Line 1 and Hologram Line 2 into a single `asteroid:floating_text` entity at a height offset of `y + 1.85`, separated by a newline (`\n`).
* **Disabled**: Spawns two distinct `asteroid:floating_text` entities. Line 1 is positioned at `y + 2.2` and Line 2 is positioned at `y + 1.8`, creating a stacked appearance.

### NPC Behavior
* **Fixed**: The NPC maintains a static rotation. You can lock this rotation to cardinal directions during placement or modify it using the Set NPC Rotation tool.
* **Look at player**: Activates an interval loop running every 2 ticks (10 times per second) that scans for the closest player within 10 blocks of the NPC and updates the NPC's rotation vector to look at them.

### Lock Facing Straight
* **Enabled**: Snaps the NPC's facing direction to the nearest cardinal quadrant (North, East, South, or West) based on the player's look direction when spawned.

### Skin Variant
* Selects the texture index (1 through 80) to apply to the NPC model.

### Interact / Punch Actions
* Accepts standard Minecraft commands (excluding the leading `/` slash). 
* Multiple commands can be chained together using a semicolon (`;`) separator (e.g., `give @s diamond; say Thanks for trading!`).
* Commands are executed through the script engine using `system.runCommandAsync` with the executor context set to the interacting player, allowing commands to run successfully even if the player does not have operator permissions.

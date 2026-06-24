import os
import sys
import uuid
import json
import shutil
import zipfile
import argparse
import base64

PACK_ICON_B64 = "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"


ANIMATION_TEMPLATE = {
    "format_version": "1.8.0",
    "animations": {
        "animation.custom_npc.idle": {
            "loop": True,
            "bones": {
                "leftArm": {
                    "rotation": [0, 0, -25]
                },
                "rightArm": {
                    "rotation": [0, 0, 25]
                }
            }
        }
    }
}

MODEL_TEMPLATE = {
    "format_version": "1.12.0",
    "minecraft:geometry": [
        {
            "description": {
                "identifier": "geometry.humanoid_custom_npc",
                "texture_width": 64,
                "texture_height": 64,
                "visible_bounds_width": 2,
                "visible_bounds_height": 3,
                "visible_bounds_offset": [0, 1.25, 0]
            },
            "bones": [
                {
                    "name": "waist",
                    "pivot": [0, 12, 0]
                },
                {
                    "name": "body",
                    "parent": "waist",
                    "pivot": [0, 24, 0],
                    "cubes": [
                        {"origin": [-4, 12, -2], "size": [8, 12, 4], "uv": [16, 16]}
                    ]
                },
                {
                    "name": "head",
                    "parent": "body",
                    "pivot": [0, 24, 0],
                    "cubes": [
                        {"origin": [-4, 24, -4], "size": [8, 8, 8], "uv": [0, 0]}
                    ]
                },
                {
                    "name": "hat",
                    "parent": "head",
                    "pivot": [0, 24, 0],
                    "cubes": [
                        {"origin": [-4, 24, -4], "size": [8, 8, 8], "inflate": 0.5, "uv": [32, 0]}
                    ]
                },
                {
                    "name": "rightArm",
                    "parent": "body",
                    "pivot": [-5, 22, 0],
                    "cubes": [
                        {"origin": [-8, 12, -2], "size": [4, 12, 4], "uv": [40, 16]}
                    ]
                },
                {
                    "name": "leftArm",
                    "parent": "body",
                    "pivot": [5, 22, 0],
                    "cubes": [
                        {"origin": [4, 12, -2], "size": [4, 12, 4], "uv": [32, 48]}
                    ]
                },
                {
                    "name": "rightLeg",
                    "parent": "waist",
                    "pivot": [-1.9, 12, 0],
                    "cubes": [
                        {"origin": [-3.9, 0, -2], "size": [4, 12, 4], "uv": [0, 16]}
                    ]
                },
                {
                    "name": "leftLeg",
                    "parent": "waist",
                    "pivot": 1.9,
                    "cubes": [
                        {"origin": [-0.1, 0, -2], "size": [4, 12, 4], "uv": [16, 48]}
                    ]
                }
            ]
        }
    ]
}

JS_TEMPLATE = """import { world, system } from "@minecraft/server";
import { ModalFormData } from "@minecraft/server-ui";

const TOTAL_SKINS = __TOTAL_SKINS__;

world.afterEvents.itemUse.subscribe((event) => {
    const player = event.source;
    const item = event.itemStack;
    if (item && item.typeId === "asteroid:npc_creator") {
        const raycast = player.getBlockFromViewDirection({ maxDistance: 10 });
        let x, y, z;
        if (raycast && raycast.block) {
            const block = raycast.block;
            x = block.x + 0.5;
            y = block.y + 1.0;
            z = block.z + 0.5;
        } else {
            const pLoc = player.location;
            x = Math.floor(pLoc.x) + 0.5;
            y = Math.floor(pLoc.y);
            z = Math.floor(pLoc.z) + 0.5;
        }
        openCreatorForm(player, null, { x, y, z });
    }
});

world.afterEvents.playerInteractWithEntity.subscribe((event) => {
    const player = event.player;
    const target = event.target;
    if (target.typeId === "asteroid:custom_npc") {
        let item = event.itemStack;
        if (!item) {
            const inv = player.getComponent("minecraft:inventory");
            if (inv && inv.container) {
                item = inv.container.getItem(player.selectedSlotIndex);
            }
        }
        if (item && item.typeId === "asteroid:npc_editor") {
            openCreatorForm(player, target, null);
        } else if (item && item.typeId === "asteroid:npc_rotator") {
            const bType = target.getDynamicProperty("behavior_type");
            if (bType === 0) {
                const dx = player.location.x - target.location.x;
                const dz = player.location.z - target.location.z;
                let rotY = Math.atan2(dz, dx) * (180 / Math.PI) - 90;
                const isLocked = target.getDynamicProperty("lock_straight");
                if (isLocked) {
                    rotY = Math.round(rotY / 90) * 90;
                }
                target.setRotation({ x: 0, y: rotY });
            }
        } else {
            const action = target.getDynamicProperty("interact_action");
            if (action && typeof action === "string" && action.trim().length > 0) {
                runAction(player, action);
            }
        }
    }
});

world.afterEvents.entityHitEntity.subscribe((event) => {
    const player = event.damagingEntity;
    const target = event.hitEntity;
    if (player && player.typeId === "minecraft:player" && target && target.typeId === "asteroid:custom_npc") {
        const action = target.getDynamicProperty("punch_action");
        if (action && typeof action === "string" && action.trim().length > 0) {
            runAction(player, action);
        }
    }
});

function runAction(player, action) {
    const cmds = action.split(";");
    for (let cmd of cmds) {
        cmd = cmd.trim();
        if (cmd.startsWith("/")) cmd = cmd.substring(1);
        if (cmd.length > 0) {
            system.runCommandAsync(`execute as "${player.name}" at @s run ${cmd}`).catch(() => {});
        }
    }
}

function openCreatorForm(player, existingEntity, spawnPos) {
    const form = new ModalFormData();
    form.title(existingEntity ? "§gNPC Editor" : "§gNPC Creator");

    let isCombined = false;
    let line1 = "";
    let line2 = "";
    let behaviorIdx = 0;
    let lockDirection = false;
    let skinIdx = 0;
    let interactAction = "";
    let punchAction = "";

    if (existingEntity) {
        const l1Val = existingEntity.getDynamicProperty("hologram_l1");
        if (l1Val !== undefined) line1 = l1Val;
        const l2Val = existingEntity.getDynamicProperty("hologram_l2");
        if (l2Val !== undefined) line2 = l2Val;
        const combVal = existingEntity.getDynamicProperty("hologram_combined");
        if (combVal !== undefined) isCombined = combVal;
        
        const bType = existingEntity.getDynamicProperty("behavior_type");
        if (bType !== undefined) behaviorIdx = bType;

        const lockVal = existingEntity.getDynamicProperty("lock_straight");
        if (lockVal !== undefined) lockDirection = lockVal;

        const currentSkin = existingEntity.getProperty("asteroid:skin_variant");
        if (currentSkin !== undefined) skinIdx = currentSkin - 1;

        const ia = existingEntity.getDynamicProperty("interact_action");
        if (ia) interactAction = ia;

        const pa = existingEntity.getDynamicProperty("punch_action");
        if (pa) punchAction = pa;
    }

    form.toggle("Combined Lines", isCombined);
    form.textField("Hologram Line 1", "Enter first line...", line1);
    form.textField("Hologram Line 2", "Enter second line...", line2);
    form.dropdown("Npc Behavior", ["Fixed", "Look at player"], behaviorIdx);
    form.toggle("Lock facing straight (N,E,S,W)", lockDirection);
    
    const skins = [];
    for (let i = 1; i <= TOTAL_SKINS; i++) {
        skins.push(`Skin ${i}`);
    }
    form.dropdown("Skin Variant", skins, skinIdx);
    form.textField("Interact Action", "Command without /", interactAction);
    form.textField("Punch Action", "Command without /", punchAction);

    system.run(() => {
        form.show(player).then((response) => {
            if (response.canceled) return;
            const [combined, l1, l2, behavior, locked, skin, interact, punch] = response.formValues;

            system.run(() => {
                let npc = existingEntity;
                if (!npc && spawnPos) {
                    const dim = player.dimension;
                    npc = dim.spawnEntity("asteroid:custom_npc", spawnPos);
                }
                
                if (npc) {
                    let finalName = l1;
                    if (l2 && l2.length > 0) {
                        finalName += combined ? "\\n" : " ";
                        finalName += l2;
                    }
                    npc.nameTag = "";
                    npc.setDynamicProperty("hologram_l1", l1);
                    npc.setDynamicProperty("hologram_l2", l2);
                    npc.setDynamicProperty("hologram_combined", combined);
                    
                    const dim = npc.dimension;
                    const texts = dim.getEntities({ type: "asteroid:floating_text", location: npc.location, maxDistance: 5, tags: [`npc_id_${npc.id}`] });
                    for (const t of texts) {
                        t.remove();
                    }
                    
                    if (combined) {
                        if (l1 || l2) {
                            let text = l1;
                            if (l2) text += "\\n" + l2;
                            const tEnt = dim.spawnEntity("asteroid:floating_text", { x: npc.location.x, y: npc.location.y + 1.85, z: npc.location.z });
                            tEnt.addTag(`npc_id_${npc.id}`);
                            tEnt.nameTag = text;
                        }
                    } else {
                        if (l1) {
                            const tEnt1 = dim.spawnEntity("asteroid:floating_text", { x: npc.location.x, y: npc.location.y + 2.2, z: npc.location.z });
                            tEnt1.addTag(`npc_id_${npc.id}`);
                            tEnt1.nameTag = l1;
                        }
                        if (l2) {
                            const tEnt2 = dim.spawnEntity("asteroid:floating_text", { x: npc.location.x, y: npc.location.y + 1.8, z: npc.location.z });
                            tEnt2.addTag(`npc_id_${npc.id}`);
                            tEnt2.nameTag = l2;
                        }
                    }
                    
                    npc.setDynamicProperty("behavior_type", behavior);
                    npc.setProperty("asteroid:skin_variant", skin + 1);
                    npc.setDynamicProperty("interact_action", interact);
                    npc.setDynamicProperty("punch_action", punch);

                    if (behavior === 1) {
                        npc.triggerEvent("asteroid:enable_look_at");
                    } else {
                        npc.triggerEvent("asteroid:disable_look_at");
                    }

                    npc.setDynamicProperty("lock_straight", locked);

                    if (behavior === 0) {
                        const dx = player.location.x - npc.location.x;
                        const dz = player.location.z - npc.location.z;
                        let rotY = Math.atan2(dz, dx) * (180 / Math.PI) - 90;
                        if (locked) {
                            rotY = Math.round(rotY / 90) * 90;
                        }
                        npc.setRotation({ x: 0, y: rotY });
                    }
                }
            });
        });
    });
}

system.runInterval(() => {
    const players = world.getAllPlayers();
    const npcs = [];
    const seen = new Set();
    for (const player of players) {
        const nearNpcs = player.dimension.getEntities({
            type: "asteroid:custom_npc",
            location: player.location,
            maxDistance: 15
        });
        for (const npc of nearNpcs) {
            if (!seen.has(npc.id)) {
                seen.add(npc.id);
                npcs.push(npc);
            }
        }
    }
    for (const npc of npcs) {
        const bType = npc.getDynamicProperty("behavior_type");
        if (bType === 1) {
            const nearPlayers = npc.dimension.getPlayers({
                location: npc.location,
                maxDistance: 10,
                closest: 1
            });
            if (nearPlayers.length > 0) {
                const closestPlayer = nearPlayers[0];
                const dx = closestPlayer.location.x - npc.location.x;
                const dz = closestPlayer.location.z - npc.location.z;
                const rotY = Math.atan2(dz, dx) * (180 / Math.PI) - 90;
                npc.setRotation({ x: 0, y: rotY });
            }
        }
    }
}, 2);
"""

def print_progress(step, message):
    print(f"[{step}/6] {message}")

def generate_packs(skins_folder, output_name):
    if not os.path.isdir(skins_folder):
        print(f"Error: Directory '{skins_folder}' not found.")
        sys.exit(1)

    images = [f for f in os.listdir(skins_folder) if f.lower().endswith('.png')]
    images.sort()
    num_skins = len(images)

    if num_skins == 0:
        print("Error: No PNG skin files found in the target directory.")
        sys.exit(1)

    print(f"Total target skins discovered: {num_skins}")
    print("-" * 50)

    build_dir = "build_temp"
    bp_dir = os.path.join(build_dir, "Asteroid_Npcs_BP")
    rp_dir = os.path.join(build_dir, "Asteroid_Npcs_RP")

    print_progress(1, "Creating folder trees...")
    os.makedirs(os.path.join(bp_dir, "entities"), exist_ok=True)
    os.makedirs(os.path.join(bp_dir, "items"), exist_ok=True)
    os.makedirs(os.path.join(bp_dir, "scripts"), exist_ok=True)

    os.makedirs(os.path.join(rp_dir, "entity"), exist_ok=True)
    os.makedirs(os.path.join(rp_dir, "models", "entity"), exist_ok=True)
    os.makedirs(os.path.join(rp_dir, "animations"), exist_ok=True)
    os.makedirs(os.path.join(rp_dir, "render_controllers"), exist_ok=True)
    os.makedirs(os.path.join(rp_dir, "textures", "entity", "npc"), exist_ok=True)
    os.makedirs(os.path.join(rp_dir, "texts"), exist_ok=True)

    print_progress(2, "Generating unique UUIDs and writing manifests...")
    bp_uuid1 = str(uuid.uuid4())
    bp_uuid2 = str(uuid.uuid4())
    bp_uuid3 = str(uuid.uuid4())
    rp_uuid1 = str(uuid.uuid4())
    rp_uuid2 = str(uuid.uuid4())

    bp_manifest = {
        "format_version": 2,
        "header": {
            "name": "Asteroid Npc's BP",
            "description": f"Skins: {num_skins}. Credits: Asteroid3946",
            "uuid": bp_uuid1,
            "version": [1, 0, 0],
            "min_engine_version": [1, 20, 80]
        },
        "modules": [
            {
                "type": "data",
                "uuid": bp_uuid2,
                "version": [1, 0, 0]
            },
            {
                "type": "script",
                "language": "javascript",
                "uuid": bp_uuid3,
                "entry": "scripts/main.js",
                "version": [1, 0, 0]
            }
        ],
        "dependencies": [
            {
                "uuid": rp_uuid1,
                "version": [1, 0, 0]
            },
            {
                "module_name": "@minecraft/server",
                "version": "1.10.0"
            },
            {
                "module_name": "@minecraft/server-ui",
                "version": "1.2.0"
            }
        ]
    }

    rp_manifest = {
        "format_version": 2,
        "header": {
            "name": "Asteroid Npc's RP",
            "description": f"Skins: {num_skins}. Credits: Asteroid3946",
            "uuid": rp_uuid1,
            "version": [1, 0, 0],
            "min_engine_version": [1, 20, 80]
        },
        "modules": [
            {
                "type": "resources",
                "uuid": rp_uuid2,
                "version": [1, 0, 0]
            }
        ],
        "dependencies": [
            {
                "uuid": bp_uuid1,
                "version": [1, 0, 0]
            }
        ]
    }

    with open(os.path.join(bp_dir, "manifest.json"), "w") as f:
        json.dump(bp_manifest, f, indent=2)

    with open(os.path.join(rp_dir, "manifest.json"), "w") as f:
        json.dump(rp_manifest, f, indent=2)

    # Decode and write pack_icon.png
    icon_data = base64.b64decode(PACK_ICON_B64)
    with open(os.path.join(bp_dir, "pack_icon.png"), "wb") as f:
        f.write(icon_data)
    with open(os.path.join(rp_dir, "pack_icon.png"), "wb") as f:
        f.write(icon_data)

    print_progress(3, f"Copying and indexing {num_skins} skin files...")
    for idx, img in enumerate(images, start=1):
        src = os.path.join(skins_folder, img)
        dst = os.path.join(rp_dir, "textures", "entity", "npc", f"npc{idx}_3d.png")
        shutil.copy2(src, dst)

    print_progress(4, "Building client resource layouts (Models, Animations, Controllers)...")
    with open(os.path.join(rp_dir, "animations", "npc.animation.json"), "w") as f:
        json.dump(ANIMATION_TEMPLATE, f, indent=2)

    with open(os.path.join(rp_dir, "models", "entity", "npc.json"), "w") as f:
        json.dump(MODEL_TEMPLATE, f, indent=2)

    rp_textures = {}
    for i in range(1, num_skins + 1):
        rp_textures[f"skin{i}"] = f"textures/entity/npc/npc{i}_3d"

    rp_entity = {
        "format_version": "1.10.0",
        "minecraft:client_entity": {
            "description": {
                "identifier": "asteroid:custom_npc",
                "materials": {
                    "default": "entity_alphatest"
                },
                "textures": rp_textures,
                "geometry": {
                    "default": "geometry.humanoid_custom_npc"
                },
                "animations": {
                    "idle": "animation.custom_npc.idle"
                },
                "scripts": {
                    "initialize": [
                        "variable.texture_index = 1;"
                    ],
                    "pre_animation": [
                        "variable.texture_index = query.property('asteroid:skin_variant');"
                    ],
                    "scale": "1.0",
                    "animate": [
                        "idle"
                    ]
                },
                "render_controllers": [
                    "controller.render.custom_npc"
                ]
            }
        }
    }

    with open(os.path.join(rp_dir, "entity", "custom_npc.entity.json"), "w") as f:
        json.dump(rp_entity, f, indent=2)

    render_skins = [f"texture.skin{i}" for i in range(1, num_skins + 1)]
    render_controller = {
        "format_version": "1.10.0",
        "render_controllers": {
            "controller.render.custom_npc": {
                "arrays": {
                    "textures": {
                        "Array.skins": render_skins
                    }
                },
                "geometry": "geometry.default",
                "materials": [ { "*": "Material.default" } ],
                "textures": [ "Array.skins[variable.texture_index - 1]" ]
            }
        }
    }

    with open(os.path.join(rp_dir, "render_controllers", "npc.render_controllers.json"), "w") as f:
        json.dump(render_controller, f, indent=2)

    rp_ft_entity = {
        "format_version": "1.10.0",
        "minecraft:client_entity": {
            "description": {
                "identifier": "asteroid:floating_text",
                "materials": {
                    "default": "entity_alphatest"
                },
                "textures": {
                    "default": "textures/entity/steve"
                },
                "geometry": {
                    "default": "geometry.empty"
                },
                "render_controllers": [
                    "controller.render.default"
                ]
            }
        }
    }

    with open(os.path.join(rp_dir, "entity", "floating_text.entity.json"), "w") as f:
        json.dump(rp_ft_entity, f, indent=2)

    print_progress(5, "Building behavior component trees and JavaScript scripts...")
    bp_entity = {
        "format_version": "1.20.80",
        "minecraft:entity": {
            "description": {
                "identifier": "asteroid:custom_npc",
                "is_spawnable": True,
                "is_summonable": True,
                "properties": {
                    "asteroid:skin_variant": {
                        "type": "int",
                        "default": 1,
                        "range": [1, num_skins],
                        "client_sync": True
                    },
                    "asteroid:look_at_player": {
                        "type": "bool",
                        "default": False,
                        "client_sync": True
                    }
                }
            },
            "components": {
                "minecraft:physics": {
                    "has_gravity": True,
                    "has_collision": True
                },
                "minecraft:pushable": {
                    "is_pushable": False,
                    "is_pushable_by_piston": False
                },
                "minecraft:knockback_resistance": {
                    "value": 1.0
                },
                "minecraft:health": {
                    "value": 20,
                    "max": 20
                },
                "minecraft:damage_sensor": {
                    "triggers": [
                        {
                            "cause": "all",
                            "deals_damage": False
                        }
                    ]
                },
                "minecraft:nameable": {
                    "allow_name_tag_renaming": False,
                    "always_show": True
                },
                "minecraft:custom_hit_test": {
                    "hitboxes": [
                        {
                            "width": 0.6,
                            "height": 1.8,
                            "pivot": [0, 0.9, 0]
                        }
                    ]
                },
                "minecraft:scale": {
                    "value": 1.0
                },
                "minecraft:interact": {
                    "interactions": [
                        {
                            "on_interact": {
                                "filters": {
                                    "test": "is_family",
                                    "subject": "other",
                                    "value": "player"
                                }
                            }
                        }
                    ]
                }
            },
            "component_groups": {
                "asteroid:look_at_group": {
                    "minecraft:lookat": {
                        "search_radius": 10,
                        "set_target": True,
                        "look_cooldown": 0,
                        "filters": {
                            "test": "is_family",
                            "subject": "other",
                            "value": "player"
                        }
                    }
                }
            },
            "events": {
                "asteroid:enable_look_at": {
                    "add": {
                        "component_groups": ["asteroid:look_at_group"]
                    }
                },
                "asteroid:disable_look_at": {
                    "remove": {
                        "component_groups": ["asteroid:look_at_group"]
                    }
                }
            }
        }
    }

    bp_ft_entity = {
        "format_version": "1.20.80",
        "minecraft:entity": {
            "description": {
                "identifier": "asteroid:floating_text",
                "is_spawnable": True,
                "is_summonable": True
            },
            "components": {
                "minecraft:physics": {
                    "has_gravity": False,
                    "has_collision": False
                },
                "minecraft:pushable": {
                    "is_pushable": False,
                    "is_pushable_by_piston": False
                },
                "minecraft:nameable": {
                    "allow_name_tag_renaming": False,
                    "always_show": True
                },
                "minecraft:collision_box": {
                    "width": 0,
                    "height": 0
                },
                "minecraft:scale": {
                    "value": 0.01
                },
                "minecraft:damage_sensor": {
                    "triggers": [
                        {
                            "cause": "all",
                            "deals_damage": False
                        }
                    ]
                }
            }
        }
    }

    with open(os.path.join(bp_dir, "entities", "custom_npc.json"), "w") as f:
        json.dump(bp_entity, f, indent=2)

    with open(os.path.join(bp_dir, "entities", "floating_text.json"), "w") as f:
        json.dump(bp_ft_entity, f, indent=2)

    creator_item = {
        "format_version": "1.20.80",
        "minecraft:item": {
            "description": {
                "identifier": "asteroid:npc_creator",
                "menu_category": {
                    "category": "equipment",
                    "group": "itemGroup.name.asteroid_npcs"
                }
            },
            "components": {
                "minecraft:display_name": {
                    "value": "§gNPC Creator"
                },
                "minecraft:icon": "stick",
                "minecraft:max_stack_size": 1
            }
        }
    }

    editor_item = {
        "format_version": "1.20.80",
        "minecraft:item": {
            "description": {
                "identifier": "asteroid:npc_editor",
                "menu_category": {
                    "category": "equipment",
                    "group": "itemGroup.name.asteroid_npcs"
                }
            },
            "components": {
                "minecraft:display_name": {
                    "value": "§gNPC Editor"
                },
                "minecraft:icon": "stick",
                "minecraft:max_stack_size": 1
            }
        }
    }

    rotator_item = {
        "format_version": "1.20.80",
        "minecraft:item": {
            "description": {
                "identifier": "asteroid:npc_rotator",
                "menu_category": {
                    "category": "equipment",
                    "group": "itemGroup.name.asteroid_npcs"
                }
            },
            "components": {
                "minecraft:display_name": {
                    "value": "§gSet NPC Rotation"
                },
                "minecraft:icon": "stick",
                "minecraft:max_stack_size": 1
            }
        }
    }

    with open(os.path.join(bp_dir, "items", "npc_creator.json"), "w") as f:
        json.dump(creator_item, f, indent=2)

    with open(os.path.join(bp_dir, "items", "npc_editor.json"), "w") as f:
        json.dump(editor_item, f, indent=2)

    with open(os.path.join(bp_dir, "items", "npc_rotator.json"), "w") as f:
        json.dump(rotator_item, f, indent=2)

    with open(os.path.join(rp_dir, "texts", "en_US.lang"), "w") as f:
        f.write("itemGroup.name.asteroid_npcs=Asteroid Npc's\n")
        f.write("entity.asteroid:custom_npc.name=Asteroid NPC\n")

    with open(os.path.join(rp_dir, "texts", "languages.json"), "w") as f:
        json.dump(["en_US"], f, indent=2)

    script_content = JS_TEMPLATE.replace("__TOTAL_SKINS__", str(num_skins))
    with open(os.path.join(bp_dir, "scripts", "main.js"), "w") as f:
        f.write(script_content)

    print_progress(6, "Packing Behavior and Resource packs into .mcaddon...")
    zip_filename = f"{output_name}.mcaddon"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as addon_zip:
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                archive_name = os.path.relpath(file_path, build_dir)
                addon_zip.write(file_path, archive_name)

    shutil.rmtree(build_dir)
    print("=" * 50)
    print(f"SUCCESS: Dynamic build finalized!")
    print(f"Pack saved to: {os.path.abspath(zip_filename)}")
    print("=" * 50)

if __name__ == "__main__":
    print("=" * 50)
    print("      ASTEROID CUSTOM NPC ADD-ON GENERATOR")
    print("=" * 50)

    parser = argparse.ArgumentParser(description="Asteroid NPC Addon Generator")
    parser.add_argument("folder", nargs="?", default=None, help="Path to the folder containing skin PNG images")
    parser.add_argument("--output", default="Asteroid_NPCs", help="Output name of the .mcaddon file")
    args = parser.parse_args()

    folder = args.folder
    output_name = args.output

    if not folder:
        try:
            folder = input("Please enter the path to the folder containing skin PNG images: ").strip()
            if (folder.startswith('"') and folder.endswith('"')) or (folder.startswith("'") and folder.endswith("'")):
                folder = folder[1:-1].strip()
            
            if folder:
                custom_output = input("Enter output name [default: Asteroid_NPCs]: ").strip()
                if custom_output:
                    output_name = custom_output
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)

    if not folder:
        print("Error: No folder path provided.")
        sys.exit(1)

    generate_packs(folder, output_name)
import { world, system } from "@minecraft/server";
import { ModalFormData } from "@minecraft/server-ui";

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
            let processedCmd = cmd.replace(/@s/g, `"${player.name}"`).replace(/@p/g, `"${player.name}"`);
            system.runCommandAsync(processedCmd).catch(() => {});
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
    for (let i = 1; i <= 80; i++) {
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
                        finalName += combined ? "\n" : " ";
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
                            if (l2) text += "\n" + l2;
                            const tEnt = dim.spawnEntity("asteroid:floating_text", { x: npc.location.x, y: npc.location.y + 1.85, z: npc.location.z });
                            tEnt.addTag(`npc_id_${npc.id}`);
                            tEnt.nameTag = text;
                        }
                    } else {
                        if (l1) {
                            const tEnt1 = dim.spawnEntity("asteroid:floating_text", { x: npc.location.x, y: npc.location.y + 2.0, z: npc.location.z });
                            tEnt1.addTag(`npc_id_${npc.id}`);
                            tEnt1.nameTag = l1;
                        }
                        if (l2) {
                            const tEnt2 = dim.spawnEntity("asteroid:floating_text", { x: npc.location.x, y: npc.location.y + 1.7, z: npc.location.z });
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

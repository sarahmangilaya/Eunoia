# Mathematical verification of all room bounding boxes across the museum

rooms = {
    # Central Hub
    "Rotunda": {"xmin": -8.5, "xmax": 8.5, "zmin": -8.5, "zmax": 8.5},
    
    # Wing I (East)
    "Wing I Promenade": {"xmin": 8.3, "xmax": 44.3, "zmin": -5.0, "zmax": 5.0},
    "Wing I Vestibule": {"xmin": 44.3, "xmax": 58.0, "zmin": -5.0, "zmax": 5.0},
    "Wing I Traditional Salon (N)": {"xmin": 44.0, "xmax": 60.0, "zmin": 5.0, "zmax": 22.0},
    "Wing I Character Studio (S)": {"xmin": 44.0, "xmax": 60.0, "zmin": -22.0, "zmax": -5.0},
    
    # Wing II (North)
    "Wing II Promenade": {"xmin": -4.0, "xmax": 4.0, "zmin": 8.3, "zmax": 52.0},
    "Wing II Room A (Env, W)": {"xmin": -22.0, "xmax": -4.0, "zmin": 9.5, "zmax": 25.5},
    "Wing II Room B (Int, E)": {"xmin": 4.0, "xmax": 22.0, "zmin": 9.5, "zmax": 25.5},
    "Wing II Room C (VFX, W)": {"xmin": -22.0, "xmax": -4.0, "zmin": 33.0, "zmax": 49.0},
    "Wing II Room D (Still, E)": {"xmin": 4.0, "xmax": 22.0, "zmin": 33.0, "zmax": 49.0},
    
    # Wing III (West)
    "Wing III Central Boulevard": {"xmin": -68.0, "xmax": -8.3, "zmin": -5.0, "zmax": 5.0},
    "Wing III Lunar Observatory (N1)": {"xmin": -46.0, "xmax": -28.0, "zmin": 5.0, "zmax": 23.0},
    "Wing III Wildlife Sanctuary (S1)": {"xmin": -46.0, "xmax": -28.0, "zmin": -23.0, "zmax": -5.0},
    "Wing III Portrait Salon (N2)": {"xmin": -66.0, "xmax": -48.0, "zmin": 5.0, "zmax": 23.0},
    "Wing III Materiality Gallery (S2)": {"xmin": -66.0, "xmax": -48.0, "zmin": -23.0, "zmax": -5.0},
    
    # Wing IV (North of Wing II)
    "Wing IV Cinema Atrium": {"xmin": -8.0, "xmax": 8.0, "zmin": 52.0, "zmax": 68.0},
    "Wing IV Applied Graphic Gallery (E)": {"xmin": 8.0, "xmax": 28.0, "zmin": 52.0, "zmax": 68.0},
    "Wing IV Production Design (W)": {"xmin": -28.0, "xmax": -8.0, "zmin": 52.0, "zmax": 68.0},
    "Wing IV Storyboard Grand Hall (N)": {"xmin": -28.0, "xmax": 28.0, "zmin": 68.0, "zmax": 92.0},
}

print(f"Total defined rooms: {len(rooms)}")

overlaps = []
room_names = list(rooms.keys())
for i in range(len(room_names)):
    for j in range(i + 1, len(room_names)):
        r1, r2 = room_names[i], room_names[j]
        b1, b2 = rooms[r1], rooms[r2]
        
        # Check if they share an intended boundary (like doorway connection)
        # An interior intersection means overlap in strict interior:
        x_overlap = max(0, min(b1["xmax"], b2["xmax"]) - max(b1["xmin"], b2["xmin"]))
        z_overlap = max(0, min(b1["zmax"], b2["zmax"]) - max(b1["zmin"], b2["zmin"]))
        
        # If both overlaps > 0.05, they intersect in 2D space!
        if x_overlap > 0.05 and z_overlap > 0.05:
            # Check if this is an intentional portal connection between adjacent spaces
            # Rotunda & Wing Promenades intersect at portals (which is normal)
            overlaps.append((r1, r2, x_overlap, z_overlap))

print(f"Interior overlaps found: {len(overlaps)}")
for o in overlaps:
    print(f"  Overlap: {o[0]} <---> {o[1]} (dx={o[2]:.2f}, dz={o[3]:.2f})")

if not overlaps:
    print("PERFECT! 100% DISJOINT ARCHITECTURE!")



def generate_procedural_texture(width, height, color_gradient=((0, 0, 128), (34, 139, 34), (210, 180, 140))):
    """Generates a terrain-like texture using noise and color gradients."""
    texture_data = np.zeros((width, height, 3), dtype=np.uint8)

    # Generate noise and apply color gradient based on height values
    for y in range(height):
        for x in range(width):
            # Noise-based height value
            height_value = pnoise2(x * NOISE_SCALE, y * NOISE_SCALE, octaves=NOISE_OCTAVES, persistence=NOISE_PERSISTENCE, lacunarity=NOISE_LACUNARITY)
            height_value = (height_value + 1) / 2  # Normalize to 0-1 range

            # Apply gradient color based on height value
            if height_value < 0.3:
                color = color_gradient[0]  # Water level
            elif height_value < 0.6:
                color = color_gradient[1]  # Grass level
            else:
                color = color_gradient[2]  # Mountain level
            
            texture_data[y, x] = color

    texture_image = Image.fromarray(texture_data, 'RGB')
    texture_image.save("generated_texture.png")
    return "generated_texture.png"

def generate_terrain_mesh(size=(10, 10), resolution=(50, 50), height_scale=10):
    """Generates a terrain mesh with vertices displaced by noise for elevation."""
    width, depth = size
    res_x, res_y = resolution
    vertices = []
    faces = []

    # Generate vertices with elevation using noise
    for y in range(res_y):
        for x in range(res_x):
            elevation = pnoise2(x * NOISE_SCALE, y * NOISE_SCALE, octaves=NOISE_OCTAVES, persistence=NOISE_PERSISTENCE, lacunarity=NOISE_LACUNARITY) * height_scale
            vertices.append((x * (width / res_x), y * (depth / res_y), elevation))

    # Generate faces connecting vertices
    for y in range(res_y - 1):
        for x in range(res_x - 1):
            i = x + y * res_x
            faces.append([i, i + 1, i + res_x + 1])
            faces.append([i, i + res_x + 1, i + res_x])

    # Create and return the mesh object
    terrain_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    return terrain_mesh

def apply_texture_to_mesh(mesh, texture_path):
    """Applies a UV-mapped texture to the mesh."""
    mesh.visual = trimesh.visual.texture.TextureVisuals(uv=mesh.vertices[:, :2], image=texture_path)

def export_mesh(mesh, file_path, file_type="obj"):
    """Exports the mesh to various 3D file formats."""
    if file_type == "obj":
        mesh.export(file_path + ".obj")
    elif file_type == "fbx":
        # Assuming FBX SDK or Blender processing
        mesh.export(file_path + ".fbx")
    elif file_type == "dae":
        # Use pycollada or Blender API for complex formats
        mesh.export(file_path + ".dae")
    else:
        raise ValueError("Unsupported file format")

def generate_and_export_terrain_mesh(file_path="terrain_mesh", file_type="obj"):
    """Generates a terrain mesh, applies a texture, and exports to the specified file format."""
    # Step 1: Generate texture
    texture_path = generate_procedural_texture(256, 256)

    # Step 2: Generate mesh
    terrain_mesh = generate_terrain_mesh(size=(100, 100), resolution=(100, 100), height_scale=10)

    # Step 3: Apply texture to mesh
    apply_texture_to_mesh(terrain_mesh, texture_path)

    # Step 4: Export to specified format
    export_mesh(terrain_mesh, file_path, file_type)
    print(f"Terrain mesh with texture exported as {file_path}.{file_type}")

# Run the generation and export
generate_and_export_terrain_mesh("exported_terrain", "obj")



def generate_texture_from_gan(model, noise_input):
    """Generates a texture using a pre-trained GAN model."""
    generated_image = model(noise_input)  # Assume GAN model is pre-trained
    texture = tf.image.convert_image_dtype(generated_image, tf.uint8)
    texture = tf.image.encode_png(texture)
    with open("generated_texture.png", "wb") as f:
        f.write(texture.numpy())
    return "generated_texture.png"

def create_terrain_entity_with_texture(height_map_path, texture_path):
    """Creates a terrain entity and applies the generated texture."""
    terrain_entity_id = editor.ToolsApplicationRequestBus(
        editor.ToolsApplicationRequestBus.Broadcast, "CreateNewEntity", entity.EntityId()
    )
    if terrain_entity_id.IsValid():
        editor.EditorEntityAPIBus(editor.EditorEntityAPIBus.Event, "SetName", terrain_entity_id, "AITerrain")
        
        # Add mesh component for the height map
        mesh_component = editor.EditorComponentAPIBus(
            editor.EditorComponentAPIBus.Broadcast, "AddComponentOfType", terrain_entity_id, MESH_COMPONENT_UUID
        )
        
        # Add material component for the texture
        material_component = editor.EditorComponentAPIBus(
            editor.EditorComponentAPIBus.Broadcast, "AddComponentOfType", terrain_entity_id, MATERIAL_COMPONENT_UUID
        )
        
        # Set the texture as material
        if material_component:
            editor.EditorComponentAPIBus(
                editor.EditorComponentAPIBus.Broadcast, "SetComponentProperty", material_component, "MaterialAsset", texture_path
            )
            print("Applied AI-generated texture to terrain.")


def add_sunlight():
    """Adds a sunlight entity."""
    sun_entity_id = editor.ToolsApplicationRequestBus(bus.Broadcast, "CreateNewEntity", entity.EntityId())
    if sun_entity_id.IsValid():
        editor.EditorEntityAPIBus(bus.Event, "SetName", sun_entity_id, "Sunlight")
        
        transform_component = editor.EditorComponentAPIBus(bus.Broadcast, "AddComponentOfType", sun_entity_id, TRANSFORM_COMPONENT_UUID)
        light_component = editor.EditorComponentAPIBus(bus.Broadcast, "AddComponentOfType", sun_entity_id, LIGHT_COMPONENT_UUID)
        
        if light_component:
            editor.EditorComponentAPIBus(bus.Broadcast, "SetComponentProperty", light_component, "LightType", "Directional")
            print("Added sunlight entity with LightComponent")
        else:
            print("Failed to add LightComponent to sunlight entity")
    else:
        print("Failed to create sunlight entity")


def create_celestial_body(name, radius, orbit_distance, color, orbit_speed=0.1, central_position=None):
    """Creates a celestial body entity with specified properties."""
    # Ensure central_position is properly initialized
    if central_position is None:
        central_position = azlmbr.math.Vector3(0, 0, 0)

    body_entity_id = editor.ToolsApplicationRequestBus(bus.Broadcast, "CreateNewEntity", entity.EntityId())
    if body_entity_id.IsValid():
        editor.EditorEntityAPIBus(bus.Event, "SetName", body_entity_id, name)

        # Set up transformation based on central_position and orbit_distance
        position = azlmbr.math.Vector3(central_position.x + orbit_distance, central_position.y, central_position.z)
        transform_component = editor.EditorComponentAPIBus(bus.Broadcast, "AddComponentOfType", body_entity_id, TRANSFORM_COMPONENT_UUID)
        if transform_component:
            editor.EditorComponentAPIBus(bus.Broadcast, "SetComponentProperty", transform_component, "Local Position", position)
        else:
            print("Failed to add TransformComponent to celestial body")

        material_component = editor.EditorComponentAPIBus(bus.Broadcast, "AddComponentOfType", body_entity_id, MATERIAL_COMPONENT_UUID)
        if material_component:
            editor.EditorComponentAPIBus(bus.Broadcast, "SetComponentProperty", material_component, "MaterialAsset", color)
            print(f"Created celestial body: {name} at position {position}")
        else:
            print("Failed to add MaterialComponent to celestial body")
    else:
        print(f"Failed to create celestial body entity: {name}")


def generate_star_system(star_name, num_planets, central_position=None, radius_range=(200, 300), orbit_distance_range=(500, 2000), planet_colors=None):
    """Generates a star system with planets around a central star."""
    print(f"Generating star system '{star_name}' at {central_position}")

    if planet_colors is None:
        planet_colors = ["materials/planet_material1.azmaterial", "materials/planet_material2.azmaterial", "materials/planet_material3.azmaterial"]

    star_color = "materials/star_material.azmaterial"
    create_celestial_body(star_name, radius=random.uniform(*radius_range), orbit_distance=0, color=star_color, central_position=central_position)

    # Generate planets orbiting the central star
    for i in range(1, num_planets + 1):
        name = f"{star_name}_Planet_{i}"
        radius = random.uniform(30, 100)
        orbit_distance = random.uniform(*orbit_distance_range)
        orbit_speed = random.uniform(0.05, 0.2)  # Assign random orbital speed
        planet_color = random.choice(planet_colors)

        create_celestial_body(name, radius, orbit_distance, planet_color, orbit_speed=orbit_speed, central_position=central_position)

def generate_galaxy():
    """Generates multiple star systems with calculated positions for each."""
    distance_between_systems = 5000  # Adjust distance between star systems
    num_systems = 5  # Define the number of star systems to generate

    for i in range(num_systems):
        # Define positions as simple float variables
        x_position = float(i * distance_between_systems)
        y_position = float(i * distance_between_systems)
        z_position = 0.0  # Z-position as a float

        # Construct Vector3 right before use
        central_position = azlmbr.math.Vector3(x_position, y_position, z_position)
        
        # Generate a star system at the given central position
        star_name = f"Star_System_{i}"
        generate_star_system(star_name, num_planets=3, central_position=central_position)
        print(f"Generated star system '{star_name}' at position {central_position}")




def open_level(level_name):
    """Opens an existing level."""
    general.open_level(level_name)
    print(f"Opened level: {level_name}")


def setup_celestial_system_on_existing_level(level_name):
    open_level(level_name)
    create_terrain_from_height_map("Assets/AI_HeightMaps/generated_height_map.png")
    add_sunlight()
    generate_galaxy()  # Generate multiple star systems

# Run the setup
setup_celestial_system_on_existing_level("CelestialGeneratedLevel")

# Main function to create the level with celestial bodies
def create_level_with_celestial_system(level_name):
    open_level(level_name)
    add_terrain()
    add_sunlight()
    generate_celestial_system()  # Generate celestial bodies in the level
    print(f"Level {level_name} with celestial system setup complete")

# Run the setup
create_level_with_celestial_system("CelestialGeneratedLevel")

def save_height_map_to_image(height_map, filename="dynamic_height_map.png"):
    # Convert to 8-bit grayscale
    img = Image.fromarray((height_map * 255).astype(np.uint8), mode='L')
    img.save(filename)

save_height_map_to_image(height_map)

def generate_asset_path(asset_name="default_asset", asset_type="default"):
    base_dir = "C:/O3DE/Assets/Generated"
    date_str = datetime.now().strftime("%Y%m%d")
    directory = os.path.join(base_dir, asset_type, date_str)
    os.makedirs(directory, exist_ok=True)
    asset_path = os.path.join(directory, f"{asset_name}.asset")
    return asset_path


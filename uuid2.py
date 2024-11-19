import azlmbr.editor as editor
import azlmbr.bus as bus

# Get UUIDs for Mesh and Material Components
MESH_COMPONENT_UUID = editor.EditorComponentAPIBus(bus.Broadcast, 'FindComponentTypeIdByName', 'Mesh')
MATERIAL_COMPONENT_UUID = editor.EditorComponentAPIBus(bus.Broadcast, 'FindComponentTypeIdByName', 'Material')

print(f"Mesh Component UUID: {MESH_COMPONENT_UUID}")
print(f"Material Component UUID: {MATERIAL_COMPONENT_UUID}")

import devsim as ds

ds.create_1d_mesh(mesh="res_mesh")

ds.add_1d_mesh_line(mesh="res_mesh", pos=0.0,   ps=0.5e-4, tag="left")
ds.add_1d_mesh_line(mesh="res_mesh", pos=25e-4, ps=0.5e-4, tag="mid")
ds.add_1d_mesh_line(mesh="res_mesh", pos=50e-4, ps=0.5e-4, tag="right")

ds.add_1d_contact(
    mesh="res_mesh",
    name="left_contact",
    material="metal",
    tag="left"
)

ds.add_1d_contact(
    mesh="res_mesh",
    name="right_contact",
    material="metal",
    tag="right"
)

ds.add_1d_region(
    mesh="res_mesh",
    region="res_region",
    material="Silicon",
    tag1="left",
    tag2="right"
)

ds.finalize_mesh(mesh="res_mesh")

ds.create_device(mesh="res_mesh", device="resistor")

ds.set_parameter(
    device="resistor",
    region="res_region",
    name="ni",
    value=1e10
)


c1 = 5e17
c2 = 5e17

ds.node_model(
    device="resistor",
    region="res_region",
    name="Ndn",
    equation="ifelse(x < 25e-4, 0, 1)"
)

ds.node_model(
    device="resistor",
    region="res_region",
    name="Nap",
    equation="0"
)

ds.node_model(
    device="resistor",
    region="res_region",
    name="NDn",
    equation=f"{c1} * Ndn"
)

ds.node_model(
    device="resistor",
    region="res_region",
    name="NAp",
    equation=f"{c2} * Nap"
)

ds.node_model(
    device="resistor",
    region="res_region",
    name="NetDoping",
    equation="NDn - NAp"
)

print("Net Doping Profile (cm^-3):")
print(
    ds.get_node_model_values(
        device="resistor",
        region="res_region",
        name="NetDoping"
    )
)

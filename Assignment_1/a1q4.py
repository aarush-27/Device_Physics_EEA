import devsim as ds
import numpy as np
import matplotlib.pyplot as plt


ds.create_1d_mesh(mesh="pn_mesh")

ds.add_1d_mesh_line(mesh="pn_mesh", pos=0.0,   ps=0.5e-4, tag="left")
ds.add_1d_mesh_line(mesh="pn_mesh", pos=25e-4, ps=0.5e-4, tag="mid")
ds.add_1d_mesh_line(mesh="pn_mesh", pos=50e-4, ps=0.5e-4, tag="right")

ds.add_1d_contact(mesh="pn_mesh", name="anode",  material="metal", tag="left")
ds.add_1d_contact(mesh="pn_mesh", name="cathode", material="metal", tag="right")

ds.add_1d_region(
    mesh="pn_mesh",
    region="pn_region",
    material="Silicon",
    tag1="left",
    tag2="right"
)

ds.finalize_mesh(mesh="pn_mesh")
ds.create_device(mesh="pn_mesh", device="pn_diode")

ND = 1e17  
NA = 1e17  


ds.node_model(
    device="pn_diode",
    region="pn_region",
    name="Ndn",
    equation=f"ifelse(x < 25e-4, 0, {ND})"
)


ds.node_model(
    device="pn_diode",
    region="pn_region",
    name="Nap",
    equation=f"ifelse(x < 25e-4, {NA}, 0)"
)


ds.node_model(
    device="pn_diode",
    region="pn_region",
    name="NetDoping",
    equation="Ndn - Nap"
)



x = np.array(
    ds.get_node_model_values(
        device="pn_diode",
        region="pn_region",
        name="x"
    )
) * 1e4  

net = np.array(
    ds.get_node_model_values(
        device="pn_diode",
        region="pn_region",
        name="NetDoping"
    )
)

plt.figure()
plt.plot(x, net)
plt.xlabel("x (µm)")
plt.ylabel("Net Doping (cm⁻³)")
plt.title("Abrupt pn-Junction Doping Profile")
plt.grid(True)
plt.show()

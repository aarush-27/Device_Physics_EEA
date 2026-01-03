import devsim as ds
import numpy as np
import matplotlib.pyplot as plt



ds.create_1d_mesh(mesh="res_mesh")

ds.add_1d_mesh_line(mesh="res_mesh", pos=0.0,   ps=0.5e-4, tag="left")
ds.add_1d_mesh_line(mesh="res_mesh", pos=25e-4, ps=0.5e-4, tag="mid")
ds.add_1d_mesh_line(mesh="res_mesh", pos=50e-4, ps=0.5e-4, tag="right")

ds.add_1d_contact(mesh="res_mesh", name="left",  material="metal", tag="left")
ds.add_1d_contact(mesh="res_mesh", name="right", material="metal", tag="right")

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


ds.node_model(
    device="resistor",
    region="res_region",
    name="NetDoping",
    equation="ifelse(x < 25e-4, 0, 5e17)"
)


ds.node_model(
    device="resistor",
    region="res_region",
    name="Potential",
    equation="0"
)


ds.node_model(
    device="resistor",
    region="res_region",
    name="ElectronConc",
    equation="ifelse(NetDoping > 0, NetDoping, ni)"
)


ds.node_model(
    device="resistor",
    region="res_region",
    name="HoleConc",
    equation="ni*ni/ElectronConc"
)

x = np.array(
    ds.get_node_model_values(
        device="resistor",
        region="res_region",
        name="x"
    )
) * 1e4   

psi = np.array(
    ds.get_node_model_values(
        device="resistor",
        region="res_region",
        name="Potential"
    )
)

n = np.array(
    ds.get_node_model_values(
        device="resistor",
        region="res_region",
        name="ElectronConc"
    )
)

p = np.array(
    ds.get_node_model_values(
        device="resistor",
        region="res_region",
        name="HoleConc"
    )
)

plt.figure()
plt.plot(x, psi)
plt.xlabel("x (µm)")
plt.ylabel("Potential ψ (V)")
plt.title("Zero-Bias Electrostatic Potential")
plt.grid(True)


plt.figure()
plt.semilogy(x, n, label="Electrons")
plt.semilogy(x, p, label="Holes")
plt.xlabel("x (µm)")
plt.ylabel("Carrier Concentration (cm⁻³)")
plt.title("Zero-Bias Carrier Concentrations")
plt.legend()
plt.grid(True)
plt.show()

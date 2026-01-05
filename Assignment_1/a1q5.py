import devsim as ds
import numpy as np
import matplotlib.pyplot as plt


ds.create_1d_mesh(mesh="pn_mesh")

ds.add_1d_mesh_line(mesh="pn_mesh", pos=0.0,   ps=0.5e-4, tag="left")
ds.add_1d_mesh_line(mesh="pn_mesh", pos=25e-4, ps=0.5e-4, tag="mid")
ds.add_1d_mesh_line(mesh="pn_mesh", pos=50e-4, ps=0.5e-4, tag="right")

ds.add_1d_contact(mesh="pn_mesh", name="anode",   material="metal", tag="left")
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



ds.set_parameter(device="pn_diode", region="pn_region", name="ni", value=1e10)

VT = 0.026       
Vbi = 0.83       


ds.node_model(
    device="pn_diode",
    region="pn_region",
    name="ND",
    equation="ifelse(x < 25e-4, 0, 1e17)"
)

ds.node_model(
    device="pn_diode",
    region="pn_region",
    name="NA",
    equation="ifelse(x < 25e-4, 1e17, 0)"
)

#################################################
# 4. SPATIAL GRID
#################################################

x = np.array(
    ds.get_node_model_values(
        device="pn_diode",
        region="pn_region",
        name="x"
    )
) * 1e4  

biases = [0.0, 0.1, 0.3, 0.5, -0.1, -0.3, -0.5]



for Va in biases:


    Vj = Vbi - Va

    ds.node_model(
        device="pn_diode",
        region="pn_region",
        name="Potential",
        equation=f"ifelse(x < 25e-4, 0, -{Vj})"
    )


    if Va >= 0:
        factor = np.exp(Va / VT) - 1
    else:
        factor = 0

    ds.node_model(
        device="pn_diode",
        region="pn_region",
        name="ExcessElectron",
        equation=f"ifelse(x < 25e-4, 0, 1e10*{factor})"
    )

    ds.node_model(
        device="pn_diode",
        region="pn_region",
        name="ExcessHole",
        equation=f"ifelse(x < 25e-4, 1e10*{factor}, 0)"
    )


    psi = np.array(
        ds.get_node_model_values(
            device="pn_diode",
            region="pn_region",
            name="Potential"
        )
    )

    dn = np.array(
        ds.get_node_model_values(
            device="pn_diode",
            region="pn_region",
            name="ExcessElectron"
        )
    )

    dp = np.array(
        ds.get_node_model_values(
            device="pn_diode",
            region="pn_region",
            name="ExcessHole"
        )
    )


    plt.figure()
    plt.plot(x, psi)
    plt.xlabel("x (µm)")
    plt.ylabel("Potential ψ (V)")
    plt.title(f"Potential vs x (Va = {Va} V)")
    plt.grid(True)


    plt.figure()
    plt.semilogy(x, np.abs(dn), label="Δn (Electrons)")
    plt.semilogy(x, np.abs(dp), label="Δp (Holes)")
    plt.xlabel("x (µm)")
    plt.ylabel("Excess Carrier Concentration (cm⁻³)")
    plt.title(f"Excess Carriers vs x (Va = {Va} V)")
    plt.legend()
    plt.grid(True)
plt.show()

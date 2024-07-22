import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from typing import Literal
import math



def draw_vault_and_lamps(n_lamps: int = 7, dist_type: Literal["linear", "radial"] = "linear", padding: float = 0):
    fig, ax = plt.subplots()
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')

    VAULT_R = 1

    vault_base = plt.Rectangle((-1, -2), 2, 2, fill=True, facecolor="0.5")
    vault_top = plt.Circle((0, 0), VAULT_R, fill=True, clip_on=False, facecolor="0.5")

    ax.add_patch(vault_base)
    ax.add_patch(vault_top)

    def draw_lamp(x, y) -> None:
        STRING_W = VAULT_R / 40
        STRING_H = VAULT_R / 15

        TOP_REC_W = VAULT_R / 15
        TOP_REC_H = VAULT_R / 7

        LAMP_R = VAULT_R / 11

        BOT_REC_W = VAULT_R / 12
        BOT_REC_H = VAULT_R / 12

        string = plt.Rectangle((x - STRING_W / 2, y - STRING_H), STRING_W, STRING_H, facecolor="r")
        top_rec = plt.Rectangle((x - TOP_REC_W / 2, y - TOP_REC_H - STRING_H), TOP_REC_W, TOP_REC_H, facecolor="r")
        lamp_circle = plt.Circle((x, y - TOP_REC_H - STRING_H), LAMP_R, fill=True, clip_on=True, facecolor="r")
        bot_rec = plt.Rectangle((x - BOT_REC_W / 2, y - TOP_REC_H - 1.2 * LAMP_R - STRING_H), BOT_REC_W, BOT_REC_H, facecolor="r")

        ax.add_patch(string)
        ax.add_patch(top_rec)
        ax.add_patch(lamp_circle)
        ax.add_patch(bot_rec)

    def generate_floor_points(n_points: int, padding: float = 0) -> list[tuple[float, float]]:
        if n_points % 2 == 0:
            dist = 2/n_points
            shift = dist/2
            xs = [shift + dist*i + padding*(i+ dist) for i in range(n_points//2)]
            return [(x, 0) for x in xs] + [(-x, 0) for x in xs]
        else:
            dist = 2/n_points
            shift = 0
            xs = [shift + dist*i + padding*(i) for i in range(n_points//2 + 1)]
            return [(x, 0) for x in xs] + [(-x, 0) for x in xs]            

    def shift_floor_to_roof(points: list[tuple[float, float]]):
        shifted_points = []
        for (x, y) in points:
            x = x
            y = VAULT_R * math.sin(math.acos(min(abs(x/VAULT_R), 1)))
            shifted_points.append((x,y))
        return shifted_points

    def generate_valve_points(n_points: int) -> list[tuple[float, float]]:
        points = []
        phis = [] if n_points % 2 == 0 else [0]
        shift = 0 if n_points % 2 == 0 else (math.pi)/(2*n_points) * (0.25 + padding)/0.25
        for k in range(n_points//2):
            phi = (2*k+1)/(n_points)*(math.pi/2 + 2*math.pi*padding)
            phi += shift
            phis.append(phi)
            phis.append(-phi)

        for phi in phis:
            theta = math.pi/2 - phi

            x = VAULT_R * math.cos(theta)
            y = VAULT_R * math.sin(theta)
            points.append((x,y))
        return points

    if dist_type == "linear":
        points = generate_floor_points(n_points=n_lamps, padding=padding)
        points = shift_floor_to_roof(points=points)
    elif dist_type == "radial":
        points = generate_valve_points(n_points=number_of_lamps)
    else:
        raise RuntimeError()

    for (x, y) in points:
        draw_lamp(x=x, y=y)

    return fig

st.title("Camilla's Lamp planner 🏮")

number_of_lamps = st.slider(label="Number of lamps", max_value=12, min_value=0, value=7)
padding = st.number_input(label="Padding", min_value=-0.3, max_value=0.04, value=-0.07, step=0.01)
distance_type = st.selectbox(label="Distance Type", options=["radial", "linear"])
fig = draw_vault_and_lamps(n_lamps=number_of_lamps, padding=padding, dist_type=distance_type)
st.pyplot(fig)

import argparse
import matplotlib
matplotlib.use('TkAgg')  # GUI backend for external window
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import pandas as pd
import os

def animate_gps(ids, folder_path, time_window=[], frame_step=10, save_path=None):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Prepare the plot
    scatter = ax.scatter([], [], c=[], cmap='viridis', label="Position (colored by time)")
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Time")
    ax.set_title("Vehicle Path Over Time")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")

    # Load data for the first vehicle (assuming one vehicle for simplicity)
    veh_id = ids[0]
    csv_path = os.path.join(folder_path, f'{veh_id}.csv')
    df = pd.read_csv(csv_path)

    # Shift the time so that it starts at zero
    df["time"] = df["time"] - df["time"].min()

    # Limit the time window if specified
    if time_window:
        df = df[(df["time"] >= time_window[0]) & (df["time"] <= time_window[1])]

    # Initialize the plot limits
    ax.set_xlim(df["x_pos"].min() - 50, df["x_pos"].max() + 50)
    ax.set_ylim(df["y_pos"].min() - 50, df["y_pos"].max() + 50)

    # Add a text caption for the description
    caption = ax.text(0.5, 1.1, '', transform=ax.transAxes, ha='center', va='top', fontsize=12, color='blue')

    # Animation function
    def update(frame):
        current_df = df[df["time"] <= frame]
        scatter.set_offsets(current_df[["x_pos", "y_pos"]].values)
        scatter.set_array(current_df["time"].values)
        scatter.set_sizes(current_df["time"].values * 0.001)  # Update point size
        scatter.set_clim(df["time"].min(), df["time"].max())  # Update color limits

        # Show the latest description at this frame, if available
        desc = ""
        if not current_df.empty and "desc" in current_df.columns:
            desc = str(current_df.iloc[-1]["desc"])
        caption.set_text(desc)

        return scatter, caption

    # Create the animation
    ani = FuncAnimation(
        fig, update, 
        frames=range(0, int(df["time"].max()) + 1, frame_step), 
        interval=5, blit=True
    )

    # Save or show
    if save_path:
        print(f"Saving animation to {save_path}...")
        writer = FFMpegWriter(fps=30)
        ani.save(save_path, writer=writer)
        print("Saved.")
    else:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Animate GPS data.")

    parser.add_argument('--ids', type=str, nargs='+', required=True,
                        help='List of vehicle IDs (e.g., veh1 veh2)')
    parser.add_argument('--folder_path', type=str, required=True,
                        help='Folder path where CSV files are stored.')
    parser.add_argument('--time_window', type=float, nargs=2, default=[],
                        help='Time window to display: start_time end_time (e.g., 0 300)')
    parser.add_argument('--frame_step', type=int, default=10,
                        help='Frame step (higher = faster animation)')
    parser.add_argument('--save', type=str, default=None,
                        help='If set, path to save the animation as .mp4')

    args = parser.parse_args()

    animate_gps(args.ids, args.folder_path, args.time_window, args.frame_step, args.save)

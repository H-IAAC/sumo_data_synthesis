import argparse
import matplotlib
matplotlib.use('TkAgg')  # GUI backend for external window
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import pandas as pd
import os

def animate_gps(veh_id, folder_path, time_window=[], frame_step=10, save_path=None, start_time=7, show_desc=True):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Load data
    csv_path = os.path.join(folder_path, f'{veh_id}.csv')
    df = pd.read_csv(csv_path)

    # Normalize time
    df["time"] -= df["time"].min()

    # Filter by time window
    if time_window:
        df = df[(df["time"] >= time_window[0]) & (df["time"] <= time_window[1])]
    df.reset_index(drop=True, inplace=True)

    # Precompute all frames
    frames = list(range(0, int(df["time"].max()) + 1, frame_step))
    coords = df[["x_pos", "y_pos"]].values
    times = df["time"].values
    if show_desc:
        descs = df["desc"].values if "desc" in df.columns else [""] * len(df)

    # Plot limits
    ax.set_xlim(coords[:, 0].min() - 50, coords[:, 0].max() + 50)
    ax.set_ylim(coords[:, 1].min() - 50, coords[:, 1].max() + 50)
    ax.set_title("Vehicle Path Over Time")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")

    # Plot object
    scatter = ax.scatter([], [], c=[], cmap='viridis')
    caption = ax.text(0.5, 1.1, '', transform=ax.transAxes, ha='center', va='top', fontsize=12, color='blue')
    time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, ha='left', va='top', fontsize=12)

    def update(frame):
        idx = times <= frame
        current_coords = coords[idx]
        current_times = times[idx]
        scatter.set_offsets(current_coords)
        scatter.set_array(current_times)

        # Description and time
        if current_coords.shape[0] > 0 and show_desc:
            caption.set_text(descs[idx][-1])
        else:
            caption.set_text("")
        
        h, m = divmod(frame, 3600)
        m //= 60
        time_text.set_text(f"Time: {start_time + h}:{m:02d} h")

        return scatter, caption, time_text

    ani = FuncAnimation(fig, update, frames=frames, interval=5, blit=True)

    if save_path:
        print(f"Saving animation to {save_path}...")
        writer = FFMpegWriter(fps=30)
        ani.save(save_path, writer=writer)
        print("Saved.")
    else:
        plt.show()

    plt.close(fig)


def animate_gps_2(veh_id, folder_path, time_window=[], frame_step=60, save_path=None, start_time=7):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Load CSV data
    csv_path = os.path.join(folder_path, f'{veh_id}.csv')
    df = pd.read_csv(csv_path)

    # Normalize time to start at 0
    df["time"] = df["time"] - df["time"].min()

    # Apply time window filtering if needed
    if time_window:
        df = df[(df["time"] >= time_window[0]) & (df["time"] <= time_window[1])]

    # Downsample to reduce frame count
    df = df[df["time"] % frame_step == 0].reset_index(drop=True)

    # Set axis limits
    ax.set_xlim(df["x_pos"].min() - 50, df["x_pos"].max() + 50)
    ax.set_ylim(df["y_pos"].min() - 50, df["y_pos"].max() + 50)

    # Prepare the scatter plot
    scatter = ax.scatter([], [], c=[], cmap='viridis', s=10)
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Time")

    # Title and labels
    ax.set_title("Vehicle Path Over Time")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")

    # Text annotations
    caption = ax.text(0.5, 1.1, '', transform=ax.transAxes, ha='center', va='top', fontsize=12, color='blue')
    time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, ha='left', va='top', fontsize=12, color='black')

    # Animation update function
    def update(frame):
        current_df = df.iloc[:frame+1]
        scatter.set_offsets(current_df[["x_pos", "y_pos"]].values)
        scatter.set_array(current_df["time"].values)
        scatter.set_clim(df["time"].min(), df["time"].max())

        # Optional description
        desc = ""
        if "desc" in current_df.columns and not current_df.empty:
            desc = str(current_df.iloc[-1]["desc"])
        caption.set_text(desc)

        # Time display (in hours)
        sim_time_hours = (current_df.iloc[-1]["time"] // 3600) + start_time
        sim_time_minutes = (current_df.iloc[-1]["time"] % 3600) // 60
        time_text.set_text(f"Time: {sim_time_hours}:{sim_time_minutes:2} h")

        return scatter, caption, time_text

    # Create animation
    ani = FuncAnimation(
        fig, update, 
        frames=len(df), 
        interval=50,  # 20 fps preview
        blit=False
    )

    # Save or show
    if save_path:
        print(f"Saving animation to {save_path}...")
        writer = FFMpegWriter(fps=10)
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
    parser.add_argument('--start_time', type=int, default=7,
                    help='Time at which the simulation starts in hours. Offsetsets the start time (default: 7)')

    args = parser.parse_args()

    animate_gps_2(args.ids, args.folder_path, args.time_window, args.frame_step, args.save, args.start_time)

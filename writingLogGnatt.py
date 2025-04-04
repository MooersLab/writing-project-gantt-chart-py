#!/opt/local/bin/python3.12
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime, timedelta
from collections import namedtuple

# Create a named tuple for task data to ensure immutability
Task = namedtuple('Task', ['name', 'start', 'end', 'phase'])

# Define tasks using the immutable namedtuple
project_tasks = (
    Task("Identify central question", "2025-04-07", "2025-04-11", "Project Initiation"),
    Task("Mindmapping", "2025-04-07", "2025-04-11", "Project Initiation"),
    Task("Audience identification", "2025-04-07", "2025-04-11", "Project Initiation"),
    Task("Articulate why bother", "2025-04-07", "2025-04-11", "Project Initiation"),
    Task("Identify key experiments and results", "2025-04-07", "2025-04-11", "Project Initiation"),
    Task("Central hypothesis and Introduction", "2025-04-07", "2025-04-11", "Project Initiation"),
    Task("Alternate titles", "2025-04-07", "2025-06-01", "Project Initiation"),
    Task("Alternate keywords", "2025-04-07", "2025-07-25", "Project Initiation"),

    Task("Results writing", "2025-04-20", "2025-07-25", "Generative writing"),
    Task("Read literature and update all parts", "2025-04-07", "2025-09-28", "Generative writing"),
    Task("Discussion outline", "2025-04-20", "2025-08-01", "Generative writing"),
    Task("Discussion prose", "2025-08-01", "2025-08-20", "Generative writing"),
    Task("Reverse outline paper", "2025-08-20", "2025-08-22", "Generative writing"),
    Task("Re-writing paper", "2025-08-23", "2025-09-01", "Generative writing"),

    Task("Proofreading", "2025-09-01", "2025-09-28", "Editing"),

    Task("Manuscript submission", "2025-09-28", "2025-09-30", "Submission"),
    Task("Manuscript revision and resubmission", "2025-11-28", "2026-01-30", "Submission"),
)

# Define custom phase colors with updated categories
phase_colors = {
    "Project Initiation": "#4287f5",       # Blue
    "Research and Fig. Making": "#42c5f5",        # Light blue
    "Generative writing": "#f542bb", # Pink
    "Editing": "#9e42f5",   # Purple
    "Submission": "#e84118"       # Red
}

# Sort tasks by start date - create new tuple
sorted_tasks = tuple(sorted(project_tasks, key=lambda task: pd.Timestamp(task.start)))

# Create figure and axis
fig, ax = plt.subplots(figsize=(14, 9))

# Directly plot the sorted tasks
task_names = []
y_positions = []

for i, task in enumerate(sorted_tasks):
    # Convert dates to timestamps
    start_date = pd.Timestamp(task.start)
    end_date = pd.Timestamp(task.end)
    
    # Calculate y position (bottom to top)
    y_pos = len(sorted_tasks) - i - 1
    y_positions.append(y_pos)
    
    # Save task name for y-axis labeling
    task_names.append(task.name)
    
    # Calculate duration
    duration = (end_date - start_date).days + 1
    
    # Plot bar
    ax.barh(y_pos, 
            duration, 
            left=mdates.date2num(start_date), 
            height=0.5,
            align='center',
            color=phase_colors[task.phase],
            alpha=0.8,
            edgecolor='navy')
    
    # Add duration text
    if duration > 3:  # Only add text if bar is wide enough
        ax.text(mdates.date2num(end_date) + 1, y_pos, f"{duration} days", 
                va='center', fontsize=8)

# Set y-axis ticks and labels from the SAME iteration that created the bars
ax.set_yticks(y_positions)
ax.set_yticklabels(task_names)
ax.set_ylim(-0.5, len(sorted_tasks) - 0.5)

# Determine overall date range for x-axis
all_starts = [pd.Timestamp(task.start) for task in sorted_tasks]
all_ends = [pd.Timestamp(task.end) for task in sorted_tasks]
min_date = min(all_starts)
max_date = max(all_ends)
date_range = (max_date - min_date).days

# Format x-axis
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))  # Mondays as major ticks
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
ax.xaxis.set_minor_locator(mdates.DayLocator())  # Daily minor ticks

# Add buffer space to the x-axis
buffer_days = max(2, date_range * 0.05)  # 5% buffer, minimum 2 days
ax.set_xlim(
    mdates.date2num(min_date - pd.Timedelta(days=buffer_days)),
    mdates.date2num(max_date + pd.Timedelta(days=buffer_days))
)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add grid for better readability
ax.grid(True, axis='x', alpha=0.3)

# Set today's date for reference line
today = pd.Timestamp('2025-04-03')

# Add today vertical line
plt.axvline(x=mdates.date2num(today), color='red', linestyle='--', 
            alpha=0.7, label='Project Start')

# Add milestone for submission
submission_task = next((t for t in sorted_tasks if t.name == "Grant submission"), None)
if submission_task:
    plt.axvline(x=mdates.date2num(pd.Timestamp(submission_task.end)), 
                color='green', linestyle='--', alpha=0.7, label='Submission Date')

# Add legend for phases
used_phases = set(task.phase for task in sorted_tasks)
for phase in used_phases:
    plt.plot([], [], color=phase_colors[phase], alpha=0.8, label=phase, linewidth=8)

plt.legend(loc='upper right', title='Project Phases')

# Add title and labels
plt.title('Writing Project Timeline (April-October 2025)', fontsize=16, pad=20)
plt.xlabel('Date', fontsize=12)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# save the figure before showing the figure
plt.savefig('writingProjectXXXXGantt.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

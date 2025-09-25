import os
import math
import subprocess
from datetime import datetime
import ipynbname
import ipywidgets as widgets
from IPython.display import display, clear_output
from IPython.display import display, Markdown

def round_half_up(n, decimals=0):
    """
    Rounds positive numbers up, as a human would expect. Requires a 'fudge'
    factor denoted by + 10**-(decimals*2) to account for rounding point errors
    for example, 5.42 * 0.75 = 4.06499999999999, which would round to
    4.06 incorrectly.
    """
    if n < 0:
        raise ValueError("This function should not be used to round negative numbers")
    multiplier = 10**decimals
    return math.floor(n * multiplier + 0.5 + 10 ** -(decimals * 2)) / multiplier


def export_calc(output_dir, file_name):
    base_name = os.path.splitext(os.path.basename(file_name))[0]

    # Search for existing revisions
    existing_revisions = []
    for f in os.listdir(output_dir):
        if f.startswith(base_name) and f.endswith(".html"):
            parts = f.replace(".html", "").split("_")
            if len(parts) > 1 and parts[-1].isdigit():
                rev_num = int(parts[-1])
                existing_revisions.append((rev_num, f))

    existing_revisions.sort()

    if existing_revisions:
        latest_rev_num, latest_file = existing_revisions[-1]
        latest_file_path = os.path.join(output_dir, latest_file)
        mod_time = datetime.fromtimestamp(os.path.getmtime(latest_file_path)).strftime("%Y-%m-%d %H:%M:%S")

        msg = widgets.HTML(
            f"<b>Latest revision:</b> {latest_file}<br><b>Last modified:</b> {mod_time}<br><br>What do you want to do?"
        )

        btn_overwrite = widgets.Button(description="Overwrite", button_style='danger')
        btn_new = widgets.Button(description="New Revision", button_style='success')
        btn_cancel = widgets.Button(description="Cancel", button_style='')

        output_widget = widgets.Output()

        def handle_choice(choice):
            clear_output()
            if choice == "cancel":
                print("Export cancelled.")
                return

            if choice == "overwrite":
                output_name = latest_file
            elif choice == "new":
                output_name = f"{base_name}_{latest_rev_num + 1}.html"

            output_path = os.path.join(output_dir, output_name)
            subprocess.run([
                "jupyter", "nbconvert",
                "--to", "html",
                "--output", output_name,
                "--output-dir", output_dir,
                ipynbname.name()
            ])

        def on_overwrite_clicked(b): handle_choice("overwrite")
        def on_new_clicked(b): handle_choice("new")
        def on_cancel_clicked(b): handle_choice("cancel")

        btn_overwrite.on_click(on_overwrite_clicked)
        btn_new.on_click(on_new_clicked)
        btn_cancel.on_click(on_cancel_clicked)

        button_box = widgets.HBox([btn_overwrite, btn_new, btn_cancel])
        display(widgets.VBox([msg, button_box, output_widget]))

    else:
        # No revisions yet — create first one
        output_name = f"{base_name}_1.html"
        output_path = os.path.join(output_dir, output_name)
        subprocess.run([
            "jupyter", "nbconvert",
            "--to", "html",
            "--output", output_name,
            "--output-dir", output_dir,
            ipynbname.name()
        ])

def job_number(job_id):

    date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    display(Markdown(f"""
**Job Number:** `{job_id}`
**Date Created:** `{date_created}`
    """))

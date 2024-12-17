import math
import pandas as pd

# Load tables from files (replace file paths with actual paths)
syntax_table_file = "morf_ІВАН ДРАЧ.tsv"  # Replace with your file path
main_table_file = "syntax_table.csv"  # Replace with your file path
syntax_types_file = "syntaxtypes.csv"  # Replace with your file path

main_table = pd.read_csv(main_table_file)

syntax_types = pd.read_csv(syntax_types_file)
syntax_table = pd.read_csv(syntax_table_file, sep="\t")
#
# with open(syntax_table_file, 'r', encoding='utf-8') as file:
#     lines = file.readlines()
#
# # Separate headers and data
# header1 = lines[0].strip().split('\t')
# data = lines[1:]
#
# # Process based on the headers
# syntax_table = pd.DataFrame(columns=header1)
#
# # Populate the DataFrames
# for line in data:
#     values = line.strip().split('\t')
#     if len(values) == len(header1):  # Match with the first header structure
#         syntax_table.loc[len(syntax_table)] = values
#
# syntax_table.to_csv("syntax_table.csv")
def get_color(ct):
    return syntax_types[syntax_types['ct']==ct].iloc[0]['color']

def synt_tolk(value):
    return value

def synt_vidn_tolk(value):
    return value

# Filter data based on text ID and sentence number
text_id = int("5367")  # Replace with actual text ID
sent_num = int("2")  # Replace with actual sentence number

filtered_main = main_table[
    (main_table['text_fk'] == text_id) & (main_table['sentence_number'] == sent_num)
    ]

filtered_syntax = syntax_table[
    (syntax_table['TextFK'] == text_id) & (syntax_table['sentence_number'] == sent_num)
    ].copy()

# Initialize position column
filtered_syntax['pos'] = 0

vstep = 30
canvas_id = f"s{sent_num}"
retv = [
    f"<canvas id='{canvas_id}' width='800' height='{len(filtered_main) * vstep}' class='conc_tree'></canvas>"
    f"<SCRIPT>var c = document.getElementById('{canvas_id}');"
    "var ctx = c.getContext('2d');"
    "ctx.font = '14px Arial';"
]

# Compute positions iteratively
deep = 0
was_change = True
max_pos = 0

while deep < 100 and was_change:
    deep += 1
    was_change = False
    for i in range(len(filtered_syntax)):
        for j in range(len(filtered_syntax)):
            if (
                    filtered_syntax.iloc[i, 3] == filtered_syntax.iloc[j, 2]  # Adjust column indices
                    and filtered_syntax.iloc[i]['pos'] >= filtered_syntax.iloc[j]['pos']
            ):
                filtered_syntax.at[j, 'pos'] = filtered_syntax.iloc[i]['pos'] + 1
                max_pos = max(max_pos, filtered_syntax.at[j, 'pos'])
                was_change = True

max_pos += 2

# Generate canvas drawing commands
for _, row in filtered_syntax.iterrows():
    pfrom, pto = 0, 0
    for idx, main_row in filtered_main.iterrows():
        if row[2] == main_row[0]:  # Adjust indices based on column names
            pfrom = idx
        if row[3] == main_row[0]:
            pto = idx

    retv.append("ctx.beginPath();")
    retv.append(f"ctx.strokeStyle='{get_color(row['ct'][:2])}';")
    retv.append(
        f"ctx.moveTo({row['pos'] * 20}, {pfrom * vstep + 7});"
        f"ctx.lineTo({(row['pos'] + 1) * 20}, {pto * vstep + 7});"
        "ctx.stroke();"
    )

    tga1 = math.atan(((pfrom - pto) * vstep) / 20.0)
    if pto < pfrom:
        retv.append("ctx.beginPath();")
        deltx = math.cos(tga1 - math.pi / 6) * 10
        delty = math.sin(tga1 - math.pi / 6) * 10
        retv.append(
            f"ctx.moveTo({(row['pos'] + 1) * 20 - deltx}, {pto * vstep + 7 + delty});"
            f"ctx.lineTo({(row['pos'] + 1) * 20}, {pto * vstep + 7});"
        )
        deltx = math.sin(math.pi / 2 - tga1 - math.pi / 6) * 10
        delty = math.cos(math.pi / 2 - tga1 - math.pi / 6) * 10
        retv.append(
            f"ctx.lineTo({(row['pos'] + 1) * 20 - deltx}, {pto * vstep + 7 + delty});"
            "ctx.stroke();"
        )
    else:
        tga1 = math.atan(20.0 / ((pto - pfrom) * vstep))
        deltx = math.sin(tga1 - math.pi / 6) * 10
        delty = math.cos(tga1 - math.pi / 6) * 10
        retv.append(
            f"ctx.moveTo({(row['pos'] + 1) * 20 - deltx}, {pto * vstep + 7 - delty});"
            f"ctx.lineTo({(row['pos'] + 1) * 20}, {pto * vstep + 7});"
        )
        deltx = math.cos(math.pi / 2 - tga1 - math.pi / 6) * 10
        delty = math.sin(math.pi / 2 - tga1 - math.pi / 6) * 10
        retv.append(
            f"ctx.lineTo({(row['pos'] + 1) * 20 - deltx}, {pto * vstep + 7 - delty});"
            "ctx.stroke();"
        )

    retv.append("ctx.beginPath();")
    retv.append("ctx.strokeStyle='#ccc';")
    retv.append(
        f"ctx.moveTo({(row['pos'] + 1) * 20}, {pto * vstep + 7});"
        f"ctx.lineTo({max_pos * 20 - 5}, {pto * vstep + 7});"
        "ctx.stroke();"
    )
    retv.append("ctx.fillStyle = '#000';")
    retv.append(
        f"ctx.fillText('{synt_tolk(row['ct'])}', {20 * max_pos + 160}, {pto * vstep + 12});"
    )
    retv.append("ctx.fillStyle = '#0b910b';")
    retv.append(
        f"ctx.fillText('{synt_vidn_tolk(row['vidn'])}', {20 * max_pos + 160}, {pto * vstep + 26});"
    )

retv.append("ctx.fillStyle = '#000';")
for idx, row in filtered_syntax.iterrows():
    retv.append(
        f"ctx.fillText('{row['word'].replace('\"', '\'')}', {20 * max_pos}, {idx * vstep + 12});"
    )
retv.append("</SCRIPT>")

# Output the generated HTML/JS as a single string
output_html = "\n".join(retv)
print(output_html)

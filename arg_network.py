from pyvis.network import Network
import pandas as pd
import math
from annotation_tagger import return_annotation_positions, clean_text_input


def html_network(got_data, html_file, label_dict, show_buttons=True, annotator_filter=False):
    got_net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)

    sources = got_data['Source']
    targets = got_data['Target']
    entities = set(sources.append(targets))

    for entity in entities:
        got_net.add_node(entity, label=entity, title=str(label_dict[entity]))

    if annotator_filter:
        got_data = got_data[got_data['Annotator Name'] == annotator_filter]

    sources = got_data['Source']
    targets = got_data['Target']
    weights = got_data['Weight']

    edge_data = zip(sources, targets, weights)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        got_net.add_edge(src, dst, value=w)

    if show_buttons:
        got_net.show_buttons()

    got_net.show(html_file)


def blob_range_dict(df):
    all_ranges = pd.concat([df['call_out_range'], df['target_range']], ignore_index=True)

    unique_ranges = all_ranges.sort_values(ascending=True).unique()

    unique_nodes = []

    node_num = 1
    node_start = 0
    node_end = 0

    for item in unique_ranges:
        base_range = range(node_start, node_end)

        if math.isnan(item[0]):
            unique_nodes.append(0)
        else:
            item_start = int(item[0])
            item_end = int(item[1])

            new_range = range(item_start, item_end)
            if set(new_range).intersection(base_range):
                node_end = max(item_end, node_end)
            else:
                node_start = item_start
                node_end = item_end
                node_num += 1
            unique_nodes.append(node_num)

    range_dict = {}

    for key, item in enumerate(unique_nodes):
        range_dict[unique_ranges[key]] = item

    return range_dict


def exact_range_dict(df):
    all_ranges = pd.concat([df['call_out_range'], df['target_range']], ignore_index=True)

    unique_ranges = all_ranges.sort_values(ascending=True).unique()

    unique_nodes = []

    for item in unique_ranges:
        if math.isnan(item[0]):
            unique_nodes.append("Undefined")
        else:
            unique_nodes.append(str(item))

    range_dict = {}

    for key, item in enumerate(unique_nodes):
        range_dict[unique_ranges[key]] = item

    return range_dict


base_names = ["android100", "ban100", "ipad100", "layoffs100", "twitter100"]
annotators = ['A1', 'A2', 'A3', 'A4', 'A5']
data_path = 'C:/Users/Jonathan/SkyDrive/Rutgers/Spring 2018/Independent Study/Argument Mining/Data/expert_annotated/'

clean_text = clean_text_input(base_names[0])

annotation_file = data_path + base_names[0]+".ea.txt"

annotations = pd.read_csv(annotation_file, sep='\t', error_bad_lines=False)

annotations['call_out_range'] = list(zip(annotations['Calling-out Span Start'], annotations['Calling-out Span End']))
annotations['target_range'] = list(zip(annotations['Target Span Start'], annotations['Target Span End']))

range_dict = blob_range_dict(annotations)

annotations['Target'] = annotations['call_out_range'].map(range_dict)
annotations['Source'] = annotations['target_range'].map(range_dict)
annotations['Weight'] = 1

label_dict = {}

for node_num, label in zip(annotations['Target'], annotations['Calling-out Spanned Text']):
    if node_num in label_dict.keys():
        if len(str(label)) > len(str(label_dict[node_num])):
            label_dict[node_num] = label
    else:
        label_dict[node_num] = label

for node_num, label in zip(annotations['Source'], annotations['Target Spanned Text']):
    if node_num in label_dict.keys():
        if len(str(label)) > len(str(label_dict[node_num])):
            label_dict[node_num] = label
    else:
        label_dict[node_num] = label

for annotator in annotators:
    html_file = "{0}_blob_network.html".format(annotator)
    html_network(annotations, html_file, annotator_filter=annotator, label_dict=label_dict)

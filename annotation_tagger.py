import codecs
import pandas as pd

base_names = ["android100", "ban100", "ipad100", "layoffs100", "twitter100"]
annotators = ['A1', 'A2', 'A3', 'A4', 'A5']
data_path = 'Data'


def return_annotation_positions(annotation, text):
    try:
        if text.count(annotation) == 1:
            start_index = text.index(annotation)
            end_index = start_index + len(annotation)
            return start_index, end_index
        else:
            return "ERROR", "ERROR"
    except:
        return "ERROR", "ERROR"


def clean_text_input(base_name):
    original_text_file = data_path + "/original/" + base_name + ".orig.txt"
    original_text = open(original_text_file, encoding="utf8").read()
    clean_text = ' '.join(repr(original_text).replace('\\n\\n', ' <p> ').replace('\\n', ' ').split(sep=' '))
    return clean_text


def append_tag_dictionary(tag_dictionary, start_position, end_position, annotator, annotation_id, class_type):

    start_tag = "<annotator_{0} id={1} class='{2}'>".format(annotator, annotation_id, class_type)

    if start_position in tag_dictionary:
        if start_tag not in tag_dictionary[start_position]:
            new_tags = tag_dictionary[start_position] + start_tag
            tag_dictionary[start_position] = new_tags
    else:
        tag_dictionary[start_position] = start_tag

    end_tag = "</annotator_{0}>".format(annotator)

    if end_position in tag_dictionary:
        if end_tag not in tag_dictionary[end_position]:
            new_tags = tag_dictionary[end_position] + end_tag
            tag_dictionary[end_position] = new_tags
    else:
        tag_dictionary[end_position] = end_tag


def add_annotation_tags(base_name):
    tags = {}
    clean_text = clean_text_input(base_name)
    df = pd.read_csv(data_path + "/expert_annotated/" + base_name + '.ea.txt', sep='\t', error_bad_lines=False)
    for row in df.iterrows():
        annotator_id = str(row[1]['Annotator Name'])

        callout_text = str(row[1]['Calling-out Spanned Text'])
        callout_id = str(row[1]['Knowtator Calling-out ID'])

        callout_start, callout_end = return_annotation_positions(callout_text, clean_text)

        append_tag_dictionary(tags, callout_start, callout_end, annotator_id, callout_id, "callout")

        target_text = str(row[1]['Target Spanned Text'])
        target_id = str(row[1]['Knowtator Target ID'])

        target_start, target_end = return_annotation_positions(target_text, clean_text)

        append_tag_dictionary(tags, target_start, target_end, annotator_id, target_id, "target")

    clean_text_list = list(clean_text)

    for key in tags:
        try:
            clean_text_list[key] = '{0}{1}'.format(tags[key], clean_text[key])
        except:
            continue

    tagged_text = ''.join(clean_text_list)

    return tagged_text


def export_tagged_text(base_names):
    for base_name in base_names:
        output_file = data_path + "/output/" + base_name + '_output_overlap.html'
        g = codecs.open(output_file, 'w', 'utf-8')

        tagged_text = add_annotation_tags(base_name)

        g.write('<!DOCTYPE html><html><head><link rel="stylesheet" href="styles.css"></head><body>'
                + tagged_text + '</body></html>')


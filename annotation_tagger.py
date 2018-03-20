import codecs
import pandas as pd
from dicttoxml import dicttoxml
import xml.dom.minidom

underlying_files = ["android100", "ban100", "ipad100",
                    "layoffs100", "twitter100"]
annotators = ['A1', 'A2', 'A3', 'A4', 'A5']
data_path = 'C:/Users/Jonathan/SkyDrive/Rutgers/Spring 2018/Independent Study/Argument Mining/Data'


def mark_expert_callouts(underlying_file, annotators):
    original_text_file = data_path + "/original/" + underlying_file + ".orig.txt"
    df = pd.read_csv(data_path + "/expert_annotated/" + underlying_file+'.ea.txt', sep='\t', error_bad_lines=False)
    original_text = open(original_text_file, encoding="utf8").read()
    clean_text = ' '.join(repr(original_text).replace('\\n\\n', ' <p> ').replace('\\n', ' ').split(sep=' '))
    errors = []

    for annotator in annotators:
        filtered = df[df['Annotator Name'] == annotator]
        for row in filtered.iterrows():
            annotation = str(row[1]['Calling-out Spanned Text'])
            callout_id = str(row[1]['Knowtator Calling-out ID'])
            if annotation in clean_text:
                if clean_text.count(annotation) == 1:
                    clean_text = clean_text.replace(annotation, '<mark>' + annotation + '</mark>')
                else:
                    errors.append(annotator + '\t' + callout_id + '\t' + annotation + '\t' + 'Multiple Matches' + '\n')
            else:
                errors.append(annotator + '\t' + callout_id + '\t' + annotation + '\t' + 'No Match' + '\n')
        output_file = data_path + "/output/" + underlying_file + '_output_{0}.html'.format(annotator)
        g = codecs.open(output_file, 'w', 'utf-8')
        g.write("<HTML>" + clean_text + "</HTML>")

    error_file = codecs.open(data_path + "/output/" + underlying_file + '_errors.txt', 'w', 'utf-8')

    error_file.writelines(errors)


def mark_ranges(annotation, text, text_dict):
    start_index = text.index(annotation)
    end_index = start_index + len(annotation)
    for x in range(start_index, end_index):
        text_dict[x] = text_dict[x] + 1
    return text_dict


def output_annotation_count_string(text, text_dict):
    count = 0
    output_string = "<Count_0>"
    for key, value in text_dict.items():
        if count != value:
            output_string = output_string + "</Count_{0}>".format(count)
            count = value
            output_string = output_string + "<Count_{0}>".format(count)
            output_string = output_string + text[key]
        else:
            output_string = output_string + text[key]
        if key == list(text_dict.keys())[-1]:
            output_string = output_string + "</Count_{0}>".format(count)

    return output_string


def mark_expert_callouts_overlap(underlying_file, annotators):
    original_text_file = data_path + "/original/" + underlying_file + ".orig.txt"
    df = pd.read_csv(data_path + "/expert_annotated/" + underlying_file+'.ea.txt', sep='\t', error_bad_lines=False)
    original_text = open(original_text_file, encoding="utf8").read()
    clean_text = ' '.join(repr(original_text).replace('\\n\\n', ' <p> ').replace('\\n', ' ').split(sep=' '))
    text_dict = dict.fromkeys(range(len(clean_text)), 0)
    errors = []

    for annotator in annotators:
        filtered = df[df['Annotator Name'] == annotator]
        for row in filtered.iterrows():
            annotation = str(row[1]['Calling-out Spanned Text'])
            callout_id = str(row[1]['Knowtator Calling-out ID'])
            if annotation in clean_text:
                if clean_text.count(annotation) == 1:
                    text_dict = mark_ranges(annotation, clean_text, text_dict)
                else:
                    errors.append(annotator + '\t' + callout_id + '\t' + annotation + '\t' + 'Multiple Matches' + '\n')
            else:
                errors.append(annotator + '\t' + callout_id + '\t' + annotation + '\t' + 'No Match' + '\n')

    ouput_string = output_annotation_count_string(clean_text, text_dict)

    output_file = data_path + "/output/" + underlying_file + '_output_overlap.html'
    g = codecs.open(output_file, 'w', 'utf-8')

    g.write('<!DOCTYPE html><html><head><link rel="stylesheet" href="styles.css"></head><body>'
            + ouput_string + '</body></html>')

    error_file = codecs.open(data_path + "/output/" + underlying_file + '_errors.txt', 'w', 'utf-8')

    error_file.writelines(errors)


def text_to_dictionary(text, source):
    list_of_dictionaries = []
    for order, term in enumerate(text.split(' ')):
        d = {'order': order, 'term': term, 'sources': [source]}
        list_of_dictionaries.append(d)
    return list_of_dictionaries


def expert_document_db(underlying_file, db):
    original_text_file = data_path + "/original/" + underlying_file + ".orig.txt"
    original_text = open(original_text_file, encoding="utf8").read()
    clean_text = ' '.join(repr(original_text).replace('\\n\\n', ' <p> ').replace('\\n', ' ').split(sep=' '))
    text_dictionary = text_to_dictionary(clean_text, underlying_file)
    for text_dict in text_dictionary:
        db.insert(text_dict)


def mark_callout_ids(annotation, annotation_id, text, db, Word):
    start_index = text.index(annotation)
    end_index = start_index + len(annotation)
    for x in range(start_index, end_index):
        try:
            new_callout_ids = db.search(Word.order == x)[0]['callout_ids']
            new_callout_ids.append(annotation_id)
            db.update({'callout_ids': new_callout_ids}, Word.order == x)
        except (KeyError, IndexError) as e:
            new_callout_ids = [annotation_id]
            db.update({'callout_ids': new_callout_ids}, Word.order == x)


def add_callout_ids(db, Word, underlying_file, annotators):
    original_text_file = data_path + "/original/" + underlying_file + ".orig.txt"
    df = pd.read_csv(data_path + "/expert_annotated/" + underlying_file+'.ea.txt', sep='\t', error_bad_lines=False)
    original_text = open(original_text_file, encoding="utf8").read()
    clean_text = ' '.join(repr(original_text).replace('\\n\\n', ' <p> ').replace('\\n', ' ').split(sep=' '))
    errors = []

    for annotator in annotators:
        filtered = df[df['Annotator Name'] == annotator]
        for row in filtered.iterrows():
            annotation = str(row[1]['Calling-out Spanned Text'])
            callout_id = str(row[1]['Knowtator Calling-out ID'])
            if annotation in clean_text:
                if clean_text.count(annotation) == 1:
                    mark_callout_ids(annotation, callout_id, clean_text, db, Word)
                else:
                    errors.append(annotator + '\t' + callout_id + '\t' + annotation + '\t' + 'Multiple Matches' + '\n')
            else:
                errors.append(annotator + '\t' + callout_id + '\t' + annotation + '\t' + 'No Match' + '\n')

    error_file = codecs.open(data_path + "/output/" + underlying_file + '_errors.txt', 'w', 'utf-8')

    error_file.writelines(errors)


def return_annotation_positions(annotation, text):
    if text.count(annotation) == 1:
        start_index = text.index(annotation)
        end_index = start_index + len(annotation)
        return start_index, end_index
    else:
        return "ERROR", "ERROR"


def clean_text_input(underlying_file):
    original_text_file = data_path + "/original/" + underlying_file + ".orig.txt"
    original_text = open(original_text_file, encoding="utf8").read()
    clean_text = ' '.join(repr(original_text).replace('\\n\\n', ' <p> ').replace('\\n', ' ').split(sep=' '))
    return clean_text


def append_word_doc_index(source, text, word_index):
    words = text.split(" ")
    for word in set(words):
        occurrences = [i for i, s in enumerate(words) if word in s]
        if word not in word_index:
            word_index[word] = {}
            word_index[word][source] = occurrences
        else:
            if source not in word_index[word]:
                word_index[word][source] = {}
                word_index[word][source] = occurrences
            else:
                word_index[word][source] = set(word_index[word][source] + occurrences)


def make_word_index(word_index):
    for file in underlying_files:
        append_word_doc_index(file, clean_text_input(file), word_index)


def print_sub_keys(word_index):
    for word in word_index:
        for doc in word_index.get(word):
            print("{0} - {1} - {2}".format(word, doc, word_index.get(word).get(doc)))


def dict_to_xml(dict):
    xml_from_array = dicttoxml(dict, custom_root='words', attr_type=False)
    output_xml = xml.dom.minidom.parseString(xml_from_array)
    pretty_xml_as_string = output_xml.toprettyxml()
    return pretty_xml_as_string


def append_doc_index(underlying_file, doc_index):
    original_text_file = data_path + "/original/" + underlying_file + ".orig.txt"
    original_text = open(original_text_file, encoding="utf8").read()
    clean_text = clean_text_input(underlying_file)
    doc_index[underlying_file] = {}
    doc_index[underlying_file]['original_text'] = original_text
    doc_index[underlying_file]['clean_text'] = clean_text


def make_doc_index(doc_index):
    for file in underlying_files:
        append_doc_index(file, doc_index)


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


def add_annotation_tags(underlying_file):
    tags = {}
    clean_text = clean_text_input(underlying_file)
    df = pd.read_csv(data_path + "/expert_annotated/" + underlying_file + '.ea.txt', sep='\t', error_bad_lines=False)
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


for underlying_file in underlying_files:
    output_file = data_path + "/output/" + underlying_file + '_output_overlap.html'
    g = codecs.open(output_file, 'w', 'utf-8')

    tagged_text = add_annotation_tags(underlying_file)

    g.write('<!DOCTYPE html><html><head><link rel="stylesheet" href="styles.css"></head><body>'
            + tagged_text + '</body></html>')

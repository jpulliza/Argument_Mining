from annotation_tagger import clean_text_input
import pandas as pd


def return_annotation_word_positions(annotation, text):
    try:
        annotation_list = annotation.split(" ")
        text_list = text.split(" ")
        for start_index in range(len(text_list)):
            end_index = start_index + len(annotation_list)
            if text_list[start_index:end_index] == annotation_list:
                return start_index, end_index
    except:
        return None


def add_to_annotation_dict(dict, text_range, annotator, prefix):
    for word_index in range(text_range[0], text_range[1]+1):
        if word_index in dict.keys():
            dict[word_index] = dict[word_index] + "T" + annotator
        else:
            dict[word_index] = prefix + annotator


def output_word_annotations(base_name, data_path):

    clean_text = clean_text_input(base_name)

    word_dict = dict(enumerate(clean_text.split(" ")))

    annotation_file = data_path + base_name + ".ea.txt"

    annotations = pd.read_csv(annotation_file, sep='\t', error_bad_lines=False)

    annotation_dict = dict(zip(word_dict.keys(), list("" for x in word_dict.keys())))

    for annotator in annotators:
        filtered_annotations = annotations[annotations['Annotator Name'] == annotator]

        for annotation in filtered_annotations['Target Spanned Text']:
            target_range = return_annotation_word_positions(annotation, clean_text)
            if target_range is not None:
                add_to_annotation_dict(annotation_dict, target_range, annotator, "T")

        for annotation in filtered_annotations['Calling-out Spanned Text']:
            callout_range = return_annotation_word_positions(annotation, clean_text)
            if callout_range is not None:
                add_to_annotation_dict(annotation_dict, callout_range, annotator, "C")


    output_df = pd.DataFrame({'words': pd.Series(word_dict), 'annotations': pd.Series(annotation_dict)})

    output_df.to_csv("{0}_word_annotations.csv".format(base_name))


base_names = ["android100", "ban100", "ipad100", "layoffs100", "twitter100"]
annotators = ['A1', 'A2', 'A3', 'A4', 'A5']
data_path = 'Data/expert_annotated/'

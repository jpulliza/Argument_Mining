import codecs
import pandas as pd

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


for underlying_file in underlying_files:
    mark_expert_annotations(underlying_file, annotators)

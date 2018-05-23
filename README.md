# Argument Mining

Visualizing call-outs and targets the content and comments of web documents as marked by annotators.

## Summary
Given a web document and a set of annotated targets and call-outs, how can we visualize differences between annotators (Micro View) and connections between text (Macro View)?

## Micro View

### Marking HTML
[x] For every annotator, add a tag indicating spans of call-out and target texts

[ ] Tags that indicate how many annotators marked that text, making a heat map

[ ] Drawing connections between unique Knowtator Target ID and Callout IDs, which [can then be connected using JavaScript and SVG ](https://gist.github.com/alojzije/11127839)

### Word Stacking
[x] For each word in a document, inidicate whether that has been marked by the annotator as in a call-out, target, or both.

[ ] Add frequency charts for how often each word appears in a category for each annotator

[ ] Move to HTML

## Macro View

### Node Networks
[x] Crete a network of call-outs and targets, where a span of text is a node.

    *   For text spans, created the options of exact spans of text or spans of text with any overlap.

[ ] Color code nodes and relationships based on annotators

[ ] Output network statistics on the network formed

## Assumptions and Technical Issues
*	No annotator creates overlapping targets or callouts.
*	Finding multiples of the same annotation in the text is thrown out.
*	Special characters and other errors
*	Position of CO are off, and get worse as they move along. This may be due to Mac vs. PC issue where the new line characters were handled differently.

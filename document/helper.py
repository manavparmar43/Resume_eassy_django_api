



def divide_paragraph(obj):
    words = obj.split()
    num_words = len(words)
    paragraphs = []
    current_paragraph = []
    for i in range(num_words):
        current_paragraph.append(words[i])
        if len(current_paragraph) >= 200 and '.' in words[i]:
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
    return paragraphs

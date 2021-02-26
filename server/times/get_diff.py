import difflib

def get_diff(old, new):
    old_arr = old.replace("\r\n", "\n").split("\n")
    ner_arr = new.replace("\r\n", "\n").split("\n")
    result = ""
    for line in difflib.ndiff(old_arr, ner_arr):
        if line[0] == "+":
            line = f"<pre class='diff-line added-line'>{line}</pre>"
        elif line[0] == "-":
            line = f"<pre class='diff-line deleted-line'>{line}</pre>"
        elif line[0] == "?":
            continue
        else:
            line = f"<pre class='diff-line'>{line}</pre>"
        result += line + "\n"
    return result
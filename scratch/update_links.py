with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_links = """  links: [
    { label: "ArtStation", url: "https://artstation.com" },
    { label: "Instagram",  url: "https://instagram.com" },
    { label: "LinkedIn",   url: "https://linkedin.com" },
    { label: "Contact",    url: "mailto:hello@eunoia.studio" }
  ],"""

new_links = """  links: [
    { label: "Facebook",  url: "https://www.facebook.com/baebiebabs#" },
    { label: "LinkedIn",  url: "https://www.linkedin.com/in/sarahmaemangilaya/" },
    { label: "Instagram", url: "https://www.instagram.com/babsiyayiyo.o_?cplk=M2F0dWNreTNmMm1n" },
    { label: "Cara",      url: "https://cara.app/bibimbabsartz" }
  ],"""

text_norm = text.replace('\r\n', '\n')
if old_links in text_norm:
    text_norm = text_norm.replace(old_links, new_links)
    with open('c:/Users/JM/Documents/Websites/Eunoia/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(text_norm)
    print("Links successfully updated!")
else:
    print("Error: old_links not found in text_norm")


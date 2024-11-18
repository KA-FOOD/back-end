import os
from flask import Flask, request, render_template, redirect, url_for
import pdfplumber
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Créer le dossier si nécessaire
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Vérifier si un fichier est uploadé
        if "pdffile" not in request.files:
            return "Aucun fichier sélectionné"
        
        file = request.files["pdffile"]
        if file.filename == "":
            return "Aucun fichier sélectionné"
        
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            extracted_data = extract_gunz_data(file_path)
            return render_template("reception/result.html", data=extracted_data)

    return render_template("reception/reception.html")

# def extract_data_from_pdf(file_path):
#     data = []
#     try:
#         with pdfplumber.open(file_path) as pdf:
#             for page_number, page in enumerate(pdf.pages):
#                 text = page.extract_text()
#                 print(f"Page {page_number + 1}:\n{text}\n{'-' * 50}")
#                 # Tu peux aussi écrire le texte dans un fichier pour une inspection
#                 with open(f"page_{page_number + 1}.txt", "w", encoding="utf-8") as f:
#                     f.write(text)

#                 # Extraction des informations spécifiques avec des regex
#                 articles = re.findall(r"Réf: (\w+).*?Nom: (.*?)\s+Prix: ([\d,.]+).*?Colis: (\d+)", text, re.DOTALL)
#                 for article in articles:
#                     ref, name, price, colis = article
#                     data.append({
#                         "ref": ref,
#                         "name": name,
#                         "price": price,
#                         "colis": colis,
#                     })
#     except Exception as e:
#         print(f"Erreur lors de la lecture du PDF : {e}")
#     return data

def extract_gunz_data(file_path):
    data = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                
                # Diviser en lignes pour traitement ligne par ligne
                lines = text.split("\n")
                
                for line in lines:
                    # Nettoyer les espaces multiples
                    line = " ".join(line.split())
                    
                    # Regex pour extraire les données
                    match = re.match(
                        r"^(\d+)\s+(.+?)\s+([\d,.]+)\s+\d+\s+\d+\s+(\d+)\s+([\d,.]+)\s+Netto\s+([\d,.]+)$", 
                        line
                    )
                    if match:
                        numero_article = match.group(1)
                        designation_produit = match.group(2)
                        nombre_pieces = match.group(4)
                        prix_par_piece = match.group(5)

                        data.append({
                            "numero_article": numero_article,
                            "designation_produit": designation_produit,
                            "nombre_pieces": nombre_pieces,
                            "prix_par_piece": prix_par_piece,
                        })
    except Exception as e:
        print(f"Erreur : {e}")
    return data


if __name__ == "__main__":
    app.run(debug=True)

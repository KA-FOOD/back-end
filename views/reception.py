import os
from flask import Flask, request, render_template, redirect, url_for, session, Response
import pdfplumber
import re
import csv
import io
from flask import Blueprint, render_template

reception_blueprint = Blueprint("reception", __name__)

app = Flask(__name__)
app.secret_key = "13cfc1ebd3ba359fce7bb3ccf5dd37862938d149d53d44c7"
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@reception_blueprint.route("/")
def reception():
    return render_template("reception.html")

# Créer le dossier si nécessaire
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/result", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Vérifier si un fichier est uploadé
        if "pdffile" not in request.files:
            return "Aucun fichier sélectionné"
        
        file = request.files["pdffile"]
        if file.filename == "":
            return "Aucun fichier sélectionné"
        
        if file:
            file.save(file_path)
            # Create a secure filename and path
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            extracted_data = extract_data_from_pdf(file_path)
            session["extracted_data"] = extracted_data
            return render_template("reception/result.html", data=extracted_data)

    return render_template("reception/reception.html")

def extract_data_from_pdf(file_path):
    data = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_number, page in enumerate(pdf.pages):
                text = page.extract_text()
                
                # Debug: Print raw text to see what we're getting
                print(f"Raw text from page {page_number + 1}:")
                print(text)
                
                # If you're working with tables, you can try this instead:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        # Process each row based on your PDF structure
                        # Example: assuming columns are ref, name, price, colis
                        if len(row) >= 4:  # Make sure row has enough columns
                            data.append({
                                "ref": row[0],
                                "name": row[1],
                                "price": row[2],
                                "colis": row[3]
                            })
                
                # If you still want to try regex, but with more flexible pattern:
                # Adjust this pattern based on your actual PDF format
                articles = re.findall(r"Réf: (\w+).*?Nom: (.*?)\s+Prix: ([\d,.]+).*?Colis: (\d+)", text, re.DOTALL)


                for article in articles:
                    ref, name, price, colis = article
                    if all([ref.strip(), name.strip(), price.strip(), colis.strip()]):
                        data.append({
                            "ref": ref.strip(),
                            "name": name.strip(),
                            "price": price.strip(),
                            "colis": colis.strip(),
                        })
                        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        # You might want to log the error or handle it appropriately
        raise
    
    # Debug: Print extracted data
    print("Extracted data:", data)
    return data

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


@app.route("/export_csv", methods=["GET"])
def export_csv():
    # Récupérer les données de la session
    data = session.get("extracted_data", [])
    print(data)
    # Nom du fichier CSV
    filename = "facture_export.csv"
    
    # Utiliser un générateur pour écrire ligne par ligne
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["numero_article", "designation_produit", "prix_par_piece", "nombre_pieces"])
    writer.writeheader()  # Ajouter les en-têtes
    writer.writerows(data)  # Ajouter les données
    print("Contenu du fichier CSV :", output.getvalue())    
    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response

if __name__ == "__main__":
    app.run(debug=True)
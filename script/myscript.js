const fournisseurName = document.getElementById('fournisseur_name');
const paysProvenance = document.getElementById('pays_provenance');
const paysOrigine = document.getElementById('pays_origine');
const natureTransactionA = document.getElementById('nature_transaction_a');
const valeurStockeefournisseurName = localStorage.getItem('fournisseurName');
const valeurStockeepaysProvenance = localStorage.getItem('paysProvenance');
const valeurStockeepaysOrigine = localStorage.getItem('paysOrigine');
const valeurStockeenatureTransactionA = localStorage.getItem('natureTransactionA');
window.onload = function() {
    

    if (valeurStockeefournisseurName) {
        fournisseurName.value = valeurStockeefournisseurName; // Remplit le champ avec la valeur stockée
    }
    if (valeurStockeepaysProvenance) {
        paysProvenance.value = valeurStockeepaysProvenance; // Remplit le champ avec la valeur stockée
    }
    if (valeurStockeepaysOrigine) {
        paysOrigine.value = valeurStockeepaysOrigine; // Remplit le champ avec la valeur stockée
    }
    if (valeurStockeenatureTransactionA) {
        natureTransactionA.value = valeurStockeenatureTransactionA; // Remplit le champ avec la valeur stockée
    }
}


    // Lorsque l'utilisateur sort du champ de texte, on enregistre la valeur dans le localStorage
    document.getElementById('fournisseur_name').addEventListener('blur', function() {
        localStorage.setItem('fournisseurName', fournisseurName.value);
        localStorage.setItem('paysProvenance', paysProvenance.value);
        localStorage.setItem('paysOrigine', paysOrigine.value);
        localStorage.setItem('natureTransactionA', natureTransactionA.value);
    });


    function clearLocalStorage(){
        localStorage.removeItem("fournisseurName");
        localStorage.removeItem("paysProvenance");
        localStorage.removeItem("paysOrigine");
        localStorage.removeItem("natureTransactionA");
    }

    function searchArticle() {
        const query = document.getElementById('article_search').value;
        fetch(`/search_article?query=${query}`)
            .then(response => response.json())
            .then(data => {
                const articleSelect = document.getElementById('article_id');
                articleSelect.innerHTML = '<option value="">Sélectionner un article</option>';
                data.forEach(article => {
                    const option = document.createElement('option');
                    option.value = article[0];
                    option.text = article[1];
                    articleSelect.add(option);
                });
            });
    }

    function updateNomenclature() {
        const articleSelect = document.getElementById('article_id');
        const selectedOption = articleSelect.options[articleSelect.selectedIndex];
        if (selectedOption.value) {
            fetch(`/search_article?query=${selectedOption.text}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        document.getElementById('nc8').value = data[0][2];
                    }
                });
        }
    }

    function searchFournisseur() {
        const query = document.getElementById('fournisseur_search').value;
        fetch(`/search_fournisseur?query=${query}`)
            .then(response => response.json())
            .then(data => {
                const fournisseurSelect = document.getElementById('fournisseur_name');
                fournisseurSelect.innerHTML = '<option value="">Sélectionner un fournisseur</option>';
                data.forEach(fournisseur => {
                    const option = document.createElement('option');
                    option.value = fournisseur[0];
                    option.text = fournisseur[1];
                    fournisseurSelect.add(option);
                });
            });
    }

    function updateFournisseurInfo() {
        const fournisseur = document.getElementById('fournisseur_name');
        const selectedFournisseur = fournisseur.options[fournisseur.selectedIndex];
        if (selectedFournisseur.value) {
            fetch(`/search_fournisseur?query=${selectedFournisseur.text}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        document.getElementById('pays_origine').value = data[0][2];
                        document.getElementById('nature_transaction_a').value = data[0][3];
                        document.getElementById('pays_provenance').value = data[0][2];
                    }
                });
        }
    }
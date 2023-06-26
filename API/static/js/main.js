var numberLineTable = 0;
var listData = [];
var imagePath = "";

const imageInput = document.getElementById('imgBase');

imageInput.addEventListener('change', function(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function(e) {
    const imageData = e.target.result;

    // Envoyer l'image au serveur pour enregistrement
    const formData = new FormData();
    formData.append('image', file);

    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      // Récupérer le chemin de l'image enregistrée depuis la réponse JSON
      imagePath = data.imagePath;
      // Afficher l'image depuis le chemin enregistré
      const imgElement = document.getElementById('imageUser');
      imgElement.src = imagePath;
    })
    .catch(error => {
      console.error('Une erreur s\'est produite:', error);
    });
  };

  reader.readAsDataURL(file);

});


function ManageSurface(){
    var SurfaceTotal = document.getElementById("surfaceTotal");
    var SurfaceNotUsed = document.getElementById("surfaceNotUsed");
    var SurfaceTotalUsed = document.getElementById("surfaceTotalUsed");

    if (!!SurfaceTotal.value)
    {
        SurfaceNotUsed.textContent = Number(SurfaceTotal.value) - Number(SurfaceTotalUsed.textContent);
    }
    else
    {
        SurfaceNotUsed.textContent = "Pas renseigné";
    }
}

function ShowHideDetailPiece(){
    var TypePiece=document.getElementById("typePiece");
    var SurfacePiece=document.getElementById("surfacePiece");
    var FenetrePiece=document.getElementById("fenetrePiece");
    var AddRoom=document.getElementById("addRoom");

    if (TypePiece.value == 0)
    {
        SurfacePiece.setAttribute("hidden", "hidden");
        FenetrePiece.setAttribute("hidden", "hidden");
        AddRoom.setAttribute("disabled", "disabled");
    }
    else
    {
        SurfacePiece.removeAttribute("hidden");
        FenetrePiece.removeAttribute("hidden");
        AddRoom.removeAttribute("disabled");
    }
}

function AddRoom(){
    var TypePiece=document.getElementById("typePiece");
    var SurfacePieceValue=document.getElementById("surfacePieceValue");
    var FenetrePieceValue=document.getElementById("fenetrePieceValue");

    var SurfaceNotUsed = document.getElementById("surfaceNotUsed");
    var SurfaceTotalUsed = document.getElementById("surfaceTotalUsed");
    var NbPieceGen = document.getElementById("nbPieceGen");

    var TableResume = document.getElementById("tableResume");

    NbPieceGen.textContent = Number(NbPieceGen.textContent) + 1;
    if (!SurfacePieceValue.value)
    {
        SurfacePieceValue.text = "Pas renseigné";
    }
    else
    {
        if (SurfaceNotUsed.textContent != "Pas renseigné")
        {
            if (Number(SurfaceNotUsed.textContent) - Number(SurfacePieceValue.value) >= 0)
            {
                SurfaceNotUsed.textContent = Number(SurfaceNotUsed.textContent) - Number(SurfacePieceValue.value);
            }
            else
            {
                alert("La surface de la pièce est supérieur à la surface restante. Merci de baisser sa surface ou alors augmenter la surface total")
                return;
            }
        }

        SurfacePieceValue.text = SurfacePieceValue.value;
        SurfaceTotalUsed.textContent = Number(SurfaceTotalUsed.textContent) + Number(SurfacePieceValue.value);

    }
    if (!FenetrePieceValue.value)
    {
        FenetrePieceValue.text = "Pas renseigné";
    }
    else
    {
        FenetrePieceValue.text = FenetrePieceValue.value
    }
    var line = document.createElement("tr");
    var colNumb = document.createElement("td");
    var colPiece = document.createElement("td");
    var colSurface = document.createElement("td");
    var colFenetre = document.createElement("td");
    var colDelete = document.createElement("td");
    var lien = document.createElement("button");
    var img = document.createElement("img");

    numberLineTable = Number(numberLineTable) + 1

    img.setAttribute("src","static/image/deleteIcon.jpg");
    img.setAttribute("width","25em");
    img.setAttribute("onclick","DeleteRoom(" + numberLineTable + ")");
    lien.appendChild(img);
    lien.setAttribute("type","button");
    colDelete.appendChild(lien);
    colFenetre.textContent = FenetrePieceValue.text;
    colSurface.textContent = SurfacePieceValue.text;
    colPiece.textContent = TypePiece.value;
    colNumb.textContent = numberLineTable

    if (numberLineTable % 2 == 0)
    {
        colFenetre.setAttribute("class","table-light");
        colDelete.setAttribute("class","table-light");
        colSurface.setAttribute("class","table-light");
        colPiece.setAttribute("class","table-light");
        colNumb.setAttribute("class","table-light");
    }
    else
    {
        colFenetre.setAttribute("class","table-info");
        colDelete.setAttribute("class","table-info");
        colSurface.setAttribute("class","table-info");
        colPiece.setAttribute("class","table-info");
        colNumb.setAttribute("class","table-info");
    }

    line.setAttribute("id",colNumb.textContent)
    line.appendChild(colNumb);
    line.appendChild(colPiece);
    line.appendChild(colSurface);
    line.appendChild(colFenetre);
    line.appendChild(colDelete);
    TableResume.appendChild(line);

    listData.push([numberLineTable,TypePiece.value,SurfacePieceValue.text,FenetrePieceValue.text]);

    SurfaceTotal.setAttribute("min",SurfaceTotalUsed.textContent);
}

function DeleteRoom(lineDelete){

    var LineDelete=document.getElementById(lineDelete);

    for (var i = 0; i < listData.length; i++)
    {
        if (listData[i][0] == lineDelete)
        {
            listData.splice(i,1);
        }
    }

    LineDelete.remove();

}

function SendData(){


    var SurfaceTotalSend = document.getElementById("surfaceTotal");
    var Base=document.getElementById("base");
    var Loading=document.getElementById("loading");

    Base.setAttribute("hidden", "hidden");
    Loading.removeAttribute("hidden");


    //alert("ok");




    var Data = {
        'img_plan' : imagePath,
        'surface_total' : SurfaceTotalSend.value,
        'liste_piece' : listData
    }

    //alert(Data['liste_piece']);

    fetch('/AI', {
      method: 'POST',
      body: JSON.stringify(Data),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(response => response.json())
    .then(response => {
        // Récupérer le chemin de l'image enregistrée depuis la réponse JSON
        imageIAPath1 = response.plans.plan1;
        imageIAPath2 = response.plans.plan2;
        imageIAPath3 = response.plans.plan3;
        //
        Loading.setAttribute("hidden", "hidden");
        Base.removeAttribute("hidden");


        // Afficher le modal et les images depuis le chemin enregistrer
        const dialog = document.getElementById("exampleModal");
        const closeModalBtn = document.getElementById("close-modal-btn");
        const reloadModalBtn = document.getElementById("reload-modal-btn");
        const likeModalBtn1 = document.getElementById("like1-modal-btn");
        const likeModalBtn2 = document.getElementById("like2-modal-btn");
        const likeModalBtn3 = document.getElementById("like3-modal-btn");
        const plan1 = document.getElementById("plan1");
        const plan2 = document.getElementById("plan2");
        const plan3 = document.getElementById("plan3");

        // Modifier les sources par ce qu'envoie l'IA
        plan1.setAttribute("src", imageIAPath1);
        plan2.setAttribute("src", imageIAPath2);
        plan3.setAttribute("src", imageIAPath3);

        dialog.style.display = 'block';


        closeModalBtn.addEventListener('click', function() {
            dialog.style.display = 'none';
        });


        reloadModalBtn.addEventListener('click', function() {
            dialog.style.display = 'none';
            SendData.call();
        });


        likeModalBtn1.addEventListener('click', function() {

            var Like = {
                'Like' : '1'
            }

            //alert(Data['liste_piece']);

            fetch('/like', {
              method: 'POST',
              body: JSON.stringify(Like),
              headers: {
                'Content-Type': 'application/json'
              }
            })

            var monBouton = document.getElementById('monBouton');
            monBouton.disabled = true;

        });

        likeModalBtn2.addEventListener('click', function() {


            var Like = {
                    'Like' : '2'
                }

                //alert(Data['liste_piece']);

                fetch('/like', {
                  method: 'POST',
                  body: JSON.stringify(Like),
                  headers: {
                    'Content-Type': 'application/json'
                  }
                })

                var monBouton = document.getElementById('monBouton');
                monBouton.disabled = true;

        });
        likeModalBtn3.addEventListener('click', function() {


            var Like = {
                'Like' : '3'
            }

            //alert(Data['liste_piece']);

            fetch('/like', {
              method: 'POST',
              body: JSON.stringify(Like),
              headers: {
                'Content-Type': 'application/json'
              }
            })

            var monBouton = document.getElementById('monBouton');
            monBouton.disabled = true;


        });





    })
    .catch(error => {
        console.error('Une erreur s\'est produite:', error);
        Loading.setAttribute("hidden", "hidden");
        Base.removeAttribute("hidden");
    });

}


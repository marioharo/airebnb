
function getAlbum(){
    region = document.getElementById('select_region').value // un numero (ID DE LA REGION)
    console.log(region)

    fetch(`http://localhost:8005/fetch_data/${region}`) //-> http://localhost:8000/fetch_data/1 (OJO CON EL PUERTO Y EL LOCALHOST)
    .then((response)=> response.json())
    .then((comunas) => {
      console.log(comunas)
      comunas = comunas
      renderCiudades(comunas)
    })
  };

  function renderCiudades(comunas){
    select = document.getElementById('select_comuna')
    select.innerHTML = '<option value="">----</option>'
    console.log(comunas.nombre_comuna)
    for (let comuna of comunas){

      select.innerHTML += `
                          <option value="${comuna.nombre_comuna}">${comuna.nombre_comuna}</option>
                          `
    }
  }

require([
    "esri/Map",
    "esri/views/MapView",
    "esri/Graphic",
    "esri/layers/GraphicsLayer"
], function (Map, MapView, Graphic, GraphicsLayer) {
    // Crear el mapa base
    const map = new Map({ basemap: "topo-vector" });

    // Crear la vista del mapa
    const view = new MapView({
        container: "viewDiv",
        map: map,
        center: [0, 20],
        zoom: 2
    });

    // Capa para mostrar los países
    const graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);

    // Datos de países
    const paises = [
        {
            nombre: "Chile",
            capital: "Santiago",
            densidad_poblacional: "25 per/km²",
            poblacion: "19 millones",
            superficie: "756,096 km²",
            moneda: "Peso chileno (CLP)",
            idiomas: ["Español"],
            animales_tipicos: ["Cóndor andino", "Puma", "Zorro culpeo"],
            dato_curioso: "El cóndor andino es una de las aves voladoras más grandes del mundo, con una envergadura de hasta 3.3 metros.",
            geometry: {
                type: "polygon",
                rings: [
                    [-75, -55],
                    [-70, -55],
                    [-70, -17],
                    [-75, -17],
                    [-75, -55]
                ]
            }
        },
        {
            nombre: "Argentina",
            capital: "Buenos Aires",
            densidad_poblacional: "16 per/km²",
            poblacion: "45 millones",
            superficie: "2,780,400 km²",
            moneda: "Peso argentino (ARS)",
            idiomas: ["Español"],
            animales_tipicos: ["Guanaco", "Ñandú", "Yaguareté"],
            dato_curioso: "El guanaco es una especie de camélido que puede sobrevivir en las condiciones extremas de la Puna argentina.",
            geometry: {
                type: "polygon",
                rings: [
                    [-73, -55],
                    [-53, -55],
                    [-53, -22],
                    [-73, -22],
                    [-73, -55]
                ]
            }
        },
        {
            nombre: "Brasil",
            capital: "Brasilia",
            densidad_poblacional: "25 per/km²",
            poblacion: "214 millones",
            superficie: "8,515,767 km²",
            moneda: "Real brasileño (BRL)",
            idiomas: ["Portugués"],
            animales_tipicos: ["Jaguar", "Capibara", "Tucán"],
            dato_curioso: "El jaguar es el felino más grande de América y uno de los pocos grandes felinos que disfruta nadar.",
            geometry: {
                type: "polygon",
                rings: [
                    [-73, -33],
                    [-34, -33],
                    [-34, 5],
                    [-73, 5],
                    [-73, -33]
                ]
            }
        }
    ];

    // Crear polígonos para cada país
    paises.forEach((pais) => {
        const graphic = new Graphic({
            geometry: pais.geometry,
            symbol: {
                type: "simple-fill",
                color: [51, 102, 255, 0],
                outline: null
            },
            attributes: pais,
            popupTemplate: {
                title: "{nombre}",
                content: `
                    <p><strong>Capital:</strong> {capital}</p>
                    <p><strong>Población:</strong> {poblacion}</p>
                    <p><strong>Densidad poblacional:</strong> {densidad_poblacional}</p>
                    <p><strong>Superficie:</strong> {superficie}</p>
                    <p><strong>Moneda:</strong> {moneda}</p>
                    <p><strong>Idiomas:</strong> {idiomas.join(", ")}</p>
                    <p><strong>Animales típicos:</strong> {animales_tipicos.join(", ")}</p>
                    <p><strong>Dato curioso:</strong> {dato_curioso}</p>
                `
            }
        });

        graphicsLayer.add(graphic);
    });
});

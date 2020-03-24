// Inicializamos las variables de las horas, minutos y segundos
var seconds1 = 0;
var mints1 = 0;
var hours1 = 0;

var seconds2 = 0;
var mints2 = 0;
var hours2 = 0;

// Estados del reloj
const states = {
    WAITING : 0,
    COUNTING : 1,
    PAUSED : 2,
}

// Variable de control del cronometro
var startchron = states.WAITING;

function chronometer() {
    if(startchron == states.COUNTING) {
        seconds1 += 1;       // seteamos los segundos

        // Verificaciones para actualizar los numeros
        if(seconds1 > 9) {
            seconds1 = 0;
            seconds2 += 1;
        }

        // set minutes
        if(seconds2 > 5) {
            seconds2 = 0;
            mints1 += 1;
        }

        if(mints1 > 9) {
            mints1 = 0;
            mints2 += 1;
        }

        if(mints2 > 5) {
            mints2 = 0;
            hours1 += 1;
        }

        if(hours1 > 9) {
            hours1 = 0;
            hours2 += 1;
        }

        // Se agrega la data en el front
        document.getElementById('chrono').innerHTML = '' + hours2 + hours1 + ':' + mints2 + mints1 + ':' + seconds2 + seconds1;

        // Esperamos un tiempo y se vuelve a llamar a chronometer para seguir contando
        setTimeout("chronometer()", 1000);
    }
}

// Inicia el cronometro
function startChr() { 
    if(startchron != states.COUNTING){

        startchron = states.COUNTING; 
        chronometer(); 
    }
}

// Detiene el cronometro
function stopChr() { 
    startchron = states.PAUSED; 
}

// Resetea a los valores por defecto las variables
function resetChr() {
    startchron = states.WAITING;
    
    hours2 = 0; 
    hours1 = 0; 
    mints2 = 0; 
    mints1 = 0; 
    seconds2 = 0; 
    seconds1 = 0; 
    
    document.getElementById('chrono').innerHTML = '' + hours2 + hours1 + ':' + mints2 + mints1 + ':' + seconds2 + seconds1;
}

document.getElementById('chrono').value = seconds1;

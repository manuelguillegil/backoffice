// Elementos a actualizar de la pagina
pageElement = document.getElementById('chronoPage');

// Inicializamos las variables de las horas, minutos y segundos
var seconds1 = 0;
var mints1 = 0;
var hours1 = 0;

var seconds2 = 0;
var mints2 = 0;
var hours2 = 0;

var clockString = '00:00:00';

// Estados del reloj
const states = {
    WAITING : 0,
    COUNTING : 1,
    PAUSED : 2,
}
/*
window.onload = function() {
  startChr(_initialClock);
}; */

/*$(window).bind('beforeunload', function() {
    console.log('AAAAAAAAAAAA estado del crono: '+startchron);
    console.log('AAAAAAAAAAAA count del crono: '+ clockString);
    //var aux = startchron;
    //startchron = states.PAUSED;
    var data = {'clock': clockString, 'clock_status': startchron };
    navigator.sendBeacon("/clock-play/", JSON.stringify(data));
    //saveClockState();
    //startchron = aux;
});*/

/*
window.addEventListener("unload", function logData() {
    console.log('AAAAAAAAAAAA estado del crono: '+startchron);
    console.log('AAAAAAAAAAAA count del crono: '+ clockString);
    var data = {clock: clockString, clock_status: startchron };
    //var e = navigator.sendBeacon("/clock-unload/", JSON.stringify(data));
    var e = navigator.sendBeacon("/clock-unload/", "holaaaaaaaaaaaaaaaaaaaaaaaa");
    if(e){
        console.log('se guardo en cambio de pagina chamito');
    }else{
        console.log('FFFFFFFFFFFFFFF');
    }
});
*/

window.addEventListener("unload", function logData() {
    console.log('AAAAAAAAAAAA estado del crono: '+startchron);
    console.log('AAAAAAAAAAAA count del crono: '+ clockString);
    var data = {clock : clockString, clock_status : startchron };
    return fetch(/clock-unload/, {
      method: 'POST', // or 'PUT'
      body: JSON.stringify(data), // data can be `string` or {object}!
      headers:{
        'Content-Type': 'application/json'
      }
    })
});

// Variable de control del cronometro
var startchron = states.WAITING;

function chronometer() {

    if(startchron == states.COUNTING) {
        
        increase_time();

        clockString = '' + hours2 + hours1 + ':' + mints2 + mints1 + ':' + seconds2 + seconds1;
        // Se agrega la data en el front
        document.getElementById('chrono').innerHTML = clockString;
        
        if(pageElement != null) {
            pageElement.innerHTML = clockString;
        }
        
        console.log('crono: estado del crono: '+startchron);
        console.log('crono: count del crono: '+ clockString);
        // Esperamos un tiempo y se vuelve a llamar a chronometer para seguir contando
        setTimeout("chronometer()", 1000);
    }
}

function increase_time(){
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
}

// Inicia el cronometro
async function startChr() { 

    console.log('plaaaaaaaay');

    if(startchron != states.COUNTING){

        var promise = new Promise( (resolve, reject) => {

            $.ajax({
                url: '/clock-play/',
                data: {
                    'clock': clockString, 
                    'clock_status': startchron,
                },
                type: 'POST',
                success:function(json){
                    if(json.status=='success'){
                        clockString = json.clockString;
                        startchron = json.clock_status;
                        hideWarn();
                        
                        if(clockString!=''){
                            console.log('llego: '+clockString);
                            startchron = states.COUNTING;
                            saveClockState();
                            resolve(clockString);
                        }else{
                            reject('fail to get clockString 5');
                        }
                    }
                    else if(json.status=='error'){
                        reject('fail to get clockString 4');
                    }
                    else if(json.status == 'error_task') {
                        raiseWarn();
                        reject('Error no task');
                    }
                    else if(json.status == 'error_time') {
                        reject('No Init time');
                    }
                    else{
                        alert("Respuesta indefinida");
                        console.log(json);
                        reject('fail to get clockString 3');
                    }
                  },
                  error:function(xhr, errmsg, err){
                    //raiseErr();
                    console.log(errmsg)
                    reject('fail to get clockString 2');
                  },
                dataType:'json',

            }).done(function(response){
                console.log(response);
            });

        });


        return promise.then( clockvalue => {

            clockString = clockvalue;

            seconds1 = clockString.charCodeAt(7) - "0".charCodeAt(0);
            seconds2 = clockString.charCodeAt(6) - "0".charCodeAt(0);
            mints1   = clockString.charCodeAt(4) - "0".charCodeAt(0);
            mints2   = clockString.charCodeAt(3) - "0".charCodeAt(0);
            hours1   = clockString.charCodeAt(1) - "0".charCodeAt(0);
            hours2   = clockString.charCodeAt(0) - "0".charCodeAt(0);
            
            //startchron = states.COUNTING;
            console.log('start in: estado del crono: '+startchron);
            console.log('start in: count del crono: '+ clockString);
            // saveClockState();
            console.log('start out: estado del crono: '+startchron);
            console.log('start out: count del crono: '+ clockString);
            chronometer(); 

        }).catch( e => { 
            console.log(e); 
        }); 

    }
}

// Detiene el cronometro
function stopChr() { 
    startchron = states.PAUSED;
    console.log('pause in: estado del crono: '+startchron);
    console.log('pause in: count del crono: '+ clockString);
    saveClockState();
    console.log('pause out: estado del crono: '+startchron);
    console.log('pause out: count del crono: '+ clockString);
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
    
    clockString = '' + hours2 + hours1 + ':' + mints2 + mints1 + ':' + seconds2 + seconds1;
    console.log('reset in: estado del crono: '+startchron);
    console.log('reset in: count del crono: '+ clockString);
    saveClockState();
    console.log('reset out: estado del crono: '+startchron);
    console.log('reset out: count del crono: '+ clockString);
    document.getElementById('chrono').innerHTML = clockString;
    
    if(pageElement != null) {
        pageElement.innerHTML = clockString;
    }
}

async function saveClockState() {
    console.log('save state in: estado del crono: '+startchron);
    console.log('save state in: count del crono: '+ clockString);


    var promise2 = new Promise( (resolve, reject) => {
        $.ajax({
            url: '/clock-view/',
            data: {'clock': clockString, 'clock_status': startchron },
            type: 'POST',
            dataType:'json',
            success:function(json){
                if(json.status=='success'){

                    if(clockString != ''){
                        console.log('llego: '+clockString);
                        resolve(clockString);
                    }else{
                        reject('fail to save clockString 5');
                    }
                }
                else if(json.status == 'error_task') {
                    raiseWarn();
                    reject('Error no task');
                }
                else if(json.status == 'error_time') {
                    reject('No Init time');
                }
                else if(json.status=='error'){
                    reject('fail to save clockString 4');
                }
                else{
                    alert("Respuesta indefinida");
                    console.log(json);
                    reject('fail to save clockString 3');
                }
            },
            error:function(xhr, errmsg, err){
                //raiseErr();
                //console.log(errmsg);
                reject('fail to save clockString 2 (ajax error in saveclock) '+startchron);
            },
        }).done(function(response){
            console.log(response);
        });
    });

    return promise2.then( clockvalue => {

        clockString = clockvalue;
        console.log('jeje');

    }).catch( e => { 
        console.log(e); 
    });

}

function hideWarn(){
    $('#alertMessage').addClass("d-none");
}

function raiseWarn(){
    $('#alertMessage').removeClass("d-none");
}

document.getElementById('chrono').value = seconds1;

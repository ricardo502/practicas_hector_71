function mostrarSeccion() {
    let nombre = location.hash.slice(1) || 'inicio';
    let secciones = document.querySelectorAll('main section');

    if (!document.getElementById(nombre)) {
        nombre = 'inicio';
    }

    for (let seccion of secciones) {
        seccion.hidden = seccion.id !== nombre;
    }
}

window.addEventListener('hashchange', mostrarSeccion);
mostrarSeccion();

document.getElementById('form-calculadora').onsubmit = function(evento) {
    evento.preventDefault();

    let fecha = document.getElementById('fecha-nacimiento').value;
    let nacimiento = new Date(fecha + 'T00:00:00');
    let hoy = new Date();
    let salida = document.getElementById('resultado-calculadora');

    if (isNaN(nacimiento.getTime())) {
        salida.textContent = 'Ingresa una fecha válida.';
        return;
    }

    if (nacimiento > hoy) {
        salida.textContent = 'La fecha de nacimiento no puede ser futura.';
        return;
    }

    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    let mes = hoy.getMonth() - nacimiento.getMonth();

    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
        edad--;
    }

    salida.textContent = 'Tu edad es: ' + edad + (edad === 1 ? ' año.' : ' años.');
};

document.getElementById('form-tareas').onsubmit = function(evento) {
    evento.preventDefault();

    let campo = document.getElementById('nueva-tarea');
    let texto = campo.value.trim();

    if (texto === '') {
        return;
    }

    let tarea = document.createElement('li');
    let etiqueta = document.createElement('label');
    let casilla = document.createElement('input');
    let nombre = document.createElement('span');
    let boton = document.createElement('button');

    casilla.type = 'checkbox';
    nombre.textContent = ' ' + texto;
    boton.textContent = 'Eliminar';
    boton.type = 'button';

    casilla.onchange = function() {
        nombre.classList.toggle('completada', casilla.checked);
    };

    boton.onclick = function() {
        tarea.remove();
    };

    etiqueta.append(casilla, nombre);
    tarea.append(etiqueta, boton);
    document.getElementById('lista-tareas').append(tarea);
    campo.value = '';
    campo.focus();
};

document.getElementById('form-conversor').onsubmit = function(evento) {
    evento.preventDefault();

    let valor = Number(document.getElementById('temperatura').value);
    let origen = document.getElementById('unidad-origen').value;
    let destino = document.getElementById('unidad-destino').value;
    let salida = document.getElementById('resultado-conversor');
    let celsius = valor;

    if (origen === 'F') {
        celsius = (valor - 32) * 5 / 9;
    } else if (origen === 'K') {
        celsius = valor - 273.15;
    }

    if (celsius < -273.15) {
        salida.textContent = 'La temperatura está por debajo del cero absoluto.';
        return;
    }

    let resultado = celsius;
    let unidad = '°C';

    if (destino === 'F') {
        resultado = celsius * 9 / 5 + 32;
        unidad = '°F';
    } else if (destino === 'K') {
        resultado = celsius + 273.15;
        unidad = 'K';
    }

    if (!Number.isFinite(resultado)) {
        salida.textContent = 'El resultado es demasiado grande.';
        return;
    }

    salida.textContent = 'Resultado: ' + resultado.toFixed(2) + ' ' + unidad;
};
